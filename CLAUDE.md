# Nottingville — Girls' Hostel Website

Single static HTML page. No framework, no build step. Just index.html + images/.

## Deploy
```bash
npx wrangler pages deploy . --project-name nottingville --commit-dirty=true
git push origin main
```
Wrangler OAuth already configured. If it expires: `npx wrangler login`

## Stack
- `index.html` — entire site (HTML + CSS + JS inline)
- `images/hostel-1.jpg`, `hostel-2.jpg`, `hostel-3.jpg` — hero + story photos
- Google Fonts: Cormorant Garamond (headings) + DM Sans (body)
- Cloudflare Pages (project: `nottingville`) + Domain: `nottingville.space`
- GitHub: github.com/soumyadeep-ux/nottingville

## Hostel Facts (source of truth)
- City: **DURGAPUR** — never say Kolkata
- Run by 3 mothers, for daughters (core identity)
- 60 beds (AC + Non-AC), expanding to 100
- 4 meals/day: breakfast, lunch, evening snacks+tea, dinner
- Curfew: gate closes 7 PM, opens 6 AM
- 24x7 CCTV, wardens, daily attendance register, medical support
- Locations: 10/1 Sarojini Naidu Path, 10/3 Sarojini Naidu Path, D45 Uday Shankar, 55 Tarashankar

## Contact Numbers
- +91 91266 60502 (primary, WhatsApp)
- +91 79089 78959 (Durgapur)
- +91 84361 50885
- WhatsApp link uses: `919126660502`

## Target Audience
- Primary: Students preparing for IIT JEE, NEET, AIIMS, WBJEE, BITS Pilani
- Secondary: Parents of college girls
- Nearby coaching: FIITJEE, Aakash Institute, Allen Career Institute

## Design System
- `--ochre: #C8800A` | `--terra: #B83E2C` | `--cream: #FAF6EE` | `--deep: #231008`
- Hero bg: `grayscale(100%) brightness(0.65)` for text legibility
- CRO decision: NO forms — WhatsApp tap-to-chat only (lowest friction)
- Font weights: body 400, headings Cormorant Garamond 400-600

## Gotchas
- Domain was WHOIS-suspended on first deploy — always verify registrant email before DNS changes
- Cloudflare Pages UI GitHub connect had redirect loop bug — use wrangler CLI instead
- Hero text cut off on mobile — fixed via `padding-top: 5rem` on `.hero`
- Wrangler: create project first if new: `npx wrangler pages project create nottingville --production-branch main`
- gh CLI authenticated as `soumyadeep-ux` (keyring, no token needed)
- Cloudflare DNS nameservers: `ainsley.ns.cloudflare.com`, `kobe.ns.cloudflare.com`
