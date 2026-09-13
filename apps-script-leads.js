/**
 * Nottingville Lead Capture — Google Apps Script
 *
 * Setup:
 * 1. Create a Google Sheet named "Nottingville Leads"
 * 2. Add headers in Row 1: Timestamp | Parent Name | Phone | Student Name | Class | Exam | Coaching | Move-in | Source | Page URL | CTA | Page
 * 3. Go to Extensions → Apps Script
 * 4. Paste this code, save
 * 5. FIRST deploy only: Deploy → New deployment → Web app → Execute as: Me,
 *    Access: Anyone. Then set the web app URL in BOTH index.html
 *    (window.__SHEETS_ENDPOINT) and assets/lp.js (SHEETS_ENDPOINT).
 * 6. REDEPLOYING an existing script: Deploy → Manage deployments → edit the
 *    live deployment (pencil) → Version: New version → Deploy. Do NOT use
 *    "New deployment" — it mints a fresh /exec URL while both files still
 *    point at the old one, and every lead stops logging with no error.
 */

var SHEET_ID = '1dtCbSjtWOk5kW02XS7SshApDiE6tSM9dJb4zHoH0WcI';

// Single source of truth for the columns. Order must match the appendRow below.
var HEADERS = ['Timestamp', 'Parent Name', 'Phone', 'Student Name', 'Class', 'Exam',
               'Coaching', 'Move-in', 'Source', 'Page URL', 'CTA', 'Page'];

/**
 * Write the header row if it does not already match HEADERS.
 *
 * The header row used to be typed by hand in the Sheet UI while the column list
 * lived here in code, so adding a column meant remembering to do it in two
 * places — and on 2026-09-13 CTA and Page were written to K/L with no headers
 * above them. This makes the code the single source of truth and self-heals a
 * sheet that was never updated by hand.
 */
function ensureHeaders(sheet) {
  var range = sheet.getRange(1, 1, 1, HEADERS.length);
  var current = range.getValues()[0];
  for (var i = 0; i < HEADERS.length; i++) {
    if (current[i] === HEADERS[i]) continue;
    range.setValues([HEADERS]);
    try {
      // Match the new cells to the existing header styling (ochre fill, bold).
      sheet.getRange(1, 1).copyFormatToRange(sheet, 1, HEADERS.length, 1, 1);
    } catch (e) { /* cosmetic only — never let this break lead logging */ }
    return;
  }
}

function doGet(e) {
  return handleRequest(e.parameter);
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    return handleRequest(data);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function handleRequest(data) {
  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName('Leads');
    if (!sheet) {
      sheet = ss.getSheets()[0];
    }

    ensureHeaders(sheet);

    sheet.appendRow([
      new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }),
      data.parent_name || '',
      data.phone || '',
      data.student_name || '',
      data.student_class || '',
      data.exam || '',
      data.coaching || '',
      data.move_in || '',
      data.source || 'form',
      data.page_url || '',
      data.cta || '',
      data.page || ''
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
