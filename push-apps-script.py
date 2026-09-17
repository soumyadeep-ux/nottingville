"""Push apps-script-leads.js to the live leads web app, keeping its /exec URL.

    ~/Documents/mcp-google-ads/.venv/bin/python push-apps-script.py --dry-run
    ~/Documents/mcp-google-ads/.venv/bin/python push-apps-script.py

Same result as the manual path (paste into Code.gs, then Deploy -> Manage deployments ->
edit the live deployment -> New version). It never creates a new deployment, so the
endpoint hardcoded in index.html and assets/lp.js stays valid.

Auth: the ekamoira OAuth client from ekamoira-ops SETUP.md
(~/.config/google-sheets-mcp/credentials.json) with its own Apps Script token, so the
Sheets token (token.json, spreadsheets+drive only) is never touched. The first run opens
a consent screen; sign in as soumyadeep@ekamoira.com. Requires the Apps Script API to be
enabled both on GCP project 1027361589627 and for the user at
script.google.com/home/usersettings (both done 2026-09-17).
"""
import json
import os
import sys
import time

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# The script is bound to the "Nottingville Leads" sheet, so Drive does not list it.
# Find it again via the sheet: Extensions -> Apps Script -> Project Settings -> Script ID.
SCRIPT_ID = "10c-TQoooOYJf88c0IgF9dnsB_H3r5ofSfHBETt79z5iHlk7ocOEZ_yLo"
DEPLOYMENT_ID = "AKfycbyq7qpStx1-GTw_aymixK3ZX-uvrIjDK3-3eHtigEK1txcsSN5nm5ensBU591fqln_aaw"
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps-script-leads.js")

CLIENT = os.path.expanduser("~/.config/google-sheets-mcp/credentials.json")
TOKEN = os.path.expanduser("~/.config/google-sheets-mcp/apps-script-token.json")
SCOPES = ["https://www.googleapis.com/auth/script.projects",
          "https://www.googleapis.com/auth/script.deployments"]
API = "https://script.googleapis.com/v1"


def get_creds():
    creds = Credentials.from_authorized_user_file(TOKEN, SCOPES) if os.path.exists(TOKEN) else None
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
        creds = flow.run_local_server(port=0, login_hint="soumyadeep@ekamoira.com")
    with open(TOKEN, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN, 0o600)
    return creds


def main(dry_run):
    headers = {"Authorization": f"Bearer {get_creds().token}"}

    def call(method, path, **kwargs):
        r = requests.request(method, f"{API}/projects/{SCRIPT_ID}{path}",
                             headers=headers, timeout=60, **kwargs)
        if r.status_code >= 300:
            sys.exit(f"{method} {path}: HTTP {r.status_code}\n{r.text[:2000]}")
        return r.json()

    content = call("GET", "/content")
    files = content["files"]
    backup = f"/tmp/nottingville-apps-script-backup-{int(time.time())}.json"
    with open(backup, "w") as f:
        json.dump(content, f, indent=2)
    print("backup of current code:", backup)

    server = [f for f in files if f["type"] == "SERVER_JS"]
    if len(server) != 1:
        sys.exit(f"expected one script file, found {[f['name'] for f in server]}; not guessing")

    live = next((d for d in call("GET", "/deployments").get("deployments", [])
                 if d["deploymentId"] == DEPLOYMENT_ID), None)
    if not live:
        sys.exit("the live /exec deployment is not in this project")
    # Reads straight after an update can still show the previous version for a few seconds.
    print("live deployment on version:", live["deploymentConfig"].get("versionNumber"))

    new_source = open(SOURCE).read()
    if server[0]["source"] == new_source:
        print("project code already matches apps-script-leads.js")
    if dry_run:
        return

    server[0]["source"] = new_source
    call("PUT", "/content", json={"files": files})
    version = call("POST", "/versions", json={
        "description": f"push-apps-script.py {time.strftime('%Y-%m-%d %H:%M')}"})["versionNumber"]
    call("PUT", f"/deployments/{DEPLOYMENT_ID}", json={"deploymentConfig": {
        "scriptId": SCRIPT_ID,
        "versionNumber": version,
        "manifestFileName": "appsscript",
        "description": live["deploymentConfig"].get("description", ""),
    }})
    print(f"live deployment now on version {version}; /exec URL unchanged")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
