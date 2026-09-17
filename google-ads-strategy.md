# Nottingville — Google Ads Strategy

**Account ID:** 5886623748
**Currency:** INR | **Timezone:** Asia/Calcutta
**Google Ads Tag:** AW-11090833551
**MCC:** 8952449784 (Ekamoira Marketing)
**MCP Server:** `/Users/soumyadeepmukherjee/Documents/mcp-google-ads/google_ads_server.py`

---

## ⚠️ Status: audited and changed 2026-09-17 (assets)

**Why:** owners reported fewer calls. Since Sep 13 the ₹220 budget has been used up by
4–7 PM every day. Before Sep 11, ads still showed after 8 PM on 15 of 17 full days. About
30% of call taps come from ad clicks after 5 PM. Maps taps halved (11.3 → ~5.5/day).
Sep 14–16 had 2 call taps and 0 WhatsApp taps, against ~1.9 call taps/day before. Cause:
Max Conversions is re-learning (`LEARNING_COMPOSITION_CHANGE`) after the Sep 11 changes and
bidding up to ₹43–107 per click. Landing pages were verified healthy.

**Changes applied 2026-09-17 (API, all verified; new assets under review at time of writing):**

1. `Calls from ads` (1057572880) counts calls of **30s+** (was 60s). Google forwarding numbers
   work in India (`call_view`): of 10 ad calls since June, 5 were missed and the answered ones
   ran 10–52s, so none had ever counted.
2. **One call asset:** +91 79089 78959, shown 8 AM–10 PM daily, tied to `Calls from ads`
   (asset 422231171323). Removed +91 84361 50885 and the unscheduled 79089 link.
3. **Sitelinks → landing pages** (replaced 4 homepage-anchor links, where WhatsApp still sits
   behind the 7-field form): Fees & Room Rates · Single AC Rooms · City Centre PG · Near
   Coaching Centres.
4. **Structured snippets:** Amenities (4 Meals Daily, AC Rooms, 24/7 CCTV, Women Wardens,
   Medical Support, Daily Attendance) · Types (AC Single Room, AC Double Sharing, Four
   Sharing, Non-AC Rooms).
5. **Business name** "Nottingville" + **logo** (crystal mark, 1200×1200).
6. **5 AI-generated image assets** (Google's generator, owners' login; user's decision to use
   them). The library holds 21 copies of 5 images; one per set is linked.

Unchanged by design: callouts, no price asset, no WhatsApp message asset, no lead form.

**Still open:** (a) the evening blackout. Recommended a portfolio Max Conversions strategy with a
~₹40 max CPC (`bidding_strategy.maximize_conversions.cpc_bid_ceiling_micros`); awaiting a
decision. (b) Prepaid balance ₹1,200 on Sep 17, which runs out ~Sep 22. (c) Apps Script
redeploy for the blank-row guard. (d) New class 11–12 images must be made in the Google Ads UI:
API `generateImages` returns `CUSTOMER_NOT_ALLOWLISTED_FOR_THIS_FEATURE`.

**Measure:** the last impression hour per day, and call taps (Clicks to call + website phone
taps + `call_view`). Local actions report ~3 days late.

---

## ⚠️ Status: audited and changed 2026-09-11

**Read this first. It supersedes parts of the 2026-07-22 section below** (which in turn
supersedes the 21 Mar build notes further down).

### What the post-LP window showed (28d, 2026-08-14 → 09-10, vs the 28d before the LPs)

| | Pre-LP (Jun 24–Jul 21) | Post-LP (Aug 14–Sep 10) |
|---|---|---|
| Days actually serving | 28 | **17** |
| Spend | INR 3,731 | INR 3,749 |
| Site visits (`click_type = URL_CLICKS`) | 94 | 89 |
| CPC on site visits | INR 33.6 | INR 33.5 |
| Phone-call conversions (primary) | 7 | 6 |
| WhatsApp clicks (secondary, invisible to bidding) | ~3 | **10** |
| All leads | ~10 | **16** |
| CPA the UI shows (calls only) | INR 533 | INR 625 |
| **Real CPA (calls + WhatsApp)** | ~INR 373 | **INR 234** |
| Leads per serving day | 0.36 | **0.94** |

The landing pages worked: leads +60% on flat spend in 40% fewer serving days. Two things
hide it in the account UI.

1. **The prepaid balance throttles delivery.** The account is on manual payments, topped up
   **INR 1,500 at a time** (INR 1,271.19 credited after 18% GST) roughly weekly
   (`account_budget_proposal` history: Jul 20, Jul 26, Aug 10, Aug 18, Aug 26, Sep 8). Each
   top-up lasts 5–7 days at the ~INR 220/day Max Conversions actually spends on active days,
   then ads stop: Aug 24–25 and **Aug 31–Sep 7** were dark; ads resumed the hour of the Sep 8
   top-up. 11 of 28 days dark ≈ ~10 leads lost. Check the balance with
   `account_budget.approved_spending_limit_micros − amount_served_micros` (INR 828.93 on
   2026-09-11). **Fix:** one INR 8,000 top-up per month, or automatic payments. Nothing else
   in this doc matters more.
2. **Smart Bidding is optimising on 6 of 16 leads** because WhatsApp Click is secondary
   (the 22 Jul owner decision). Pre-LP that cost little (~3 WhatsApp/month); post-LP it is
   60% of leads, and Max Conversions is learning from ~6 conversions/month, below the ~15 it
   needs. **Done 2026-09-11: WhatsApp Click set `primary_for_goal = true`** (reverses the
   22 Jul decision; agency call). `include_in_conversions_metric` is derived/immutable — it
   flipped with it. Not retroactive in reports: the Conversions column counts WhatsApp from
   2026-09-11 onward. Next step once there are 15+ conv/month: Maximize Conversion Value with
   call = 2× WhatsApp so "calls are worth more" is encoded without blinding the algorithm.
   No MCP tool for this — it was done with `_mutate(customer_id, "conversionActions", …)`
   from a one-off script (run with `GOOGLE_ADS_AUTH_TYPE=service_account`, which `.env.local`
   does not set).

Other findings:

- **60% of "clicks" are location-expansion taps** (202 of 335, INR 2.45 each, INR 494 total;
  14 call-asset clicks, 29 directions, 1 sitelink). Only 89 clicks reached the site, at
  INR 33.5 each = 79% of spend. The 15.7% CTR is inflated by the taps. Always split
  `segments.click_type` before reading clicks or CTR on this account.
- **Geo is PRESENCE_OR_INTEREST**, not the presence-only the March notes describe; 89% of spend
  was interest-matched. **The March assumption is wrong for this account** — out-of-town
  parents convert: Kolkata 4 leads / INR 769, Dhanbad 2 / 224, Asansol 2 / 303, vs Durgapur
  itself 5 / 1,642 (Jul 22–Sep 10, calls + WhatsApp). Do **not** switch to presence-only.
  Corrects Key Learning #8 below.
- **Landing-page experience still BELOW AVERAGE on 100% of scored keywords** 7 weeks after
  launch; lost IS to rank rose 42.5% → 58.9%, which is why site-visit CPC is INR 33 not the
  historical 12–20. Pages verified: HTTP 200 for AdsBot, Lighthouse desktop 97, LCP 1.0s,
  TTFB 140ms, robots allows. Not a page defect — per-keyword history rebuilding on ~90 site
  visits/month. Nothing to fix; re-read in 4 weeks.
- **Search terms are clean.** `search_term_view` disclosed ~32% of spend. Visible leaks were
  competitor brands, traveller intent (dormitory/station/homestay), flat rentals and price caps
  written with a space ("under 5 000").
- **Day-of-week flipped** vs July (then Sat/Sun best; Jul 22–Sep 10: Thu 9, Fri 8, Sat/Sun 2
  each). Both reads are noise at this volume. Keep 24/7. 01:00–07:00 IST spent INR 308 in 7
  weeks for 0 leads — not worth a schedule.
- Desktop: INR 448, 0 conv — too small to act on. Coaching Proximity: 29 impressions/28d —
  effectively dead, costs nothing, left alone.

### Changes applied 2026-09-11

1. **18 campaign negatives** (PHRASE): `dormitory`, `railway station`, `station`, `bus stand`,
   `homestay`, `bhk`, `1 bhk`, `1bhk`, `under 5 000`, `under 4000`, `under 4 000`, `dsms`,
   `boy's`, `ashirwad`, `goswami`, `maruti kunj`, `nivedita`, `second home`. Negatives 86 → 104.
2. **Removed keyword** `dormitory durgapur` (QS 1, 17 clicks / INR 170 / 0 leads in 7 weeks).
3. **13 state exclusions** (presence-based): Kerala, Tamil Nadu, Karnataka, Telangana, Andhra
   Pradesh, Puducherry, Maharashtra, Gujarat, Goa, Daman & Diu, DNH&DD, Lakshadweep, Andaman.
   Deliberately conservative — the Hindi-belt states were left in because the location data
   is thin. ~INR 300/7 weeks of spend, 1 noise lead.
4. **Three new ad groups**, each on a page that existed since Jul 22 but had no ad group:
   - **Single Room PG Durgapur** (202803692809) → `/single-room-pg-durgapur`, 10 keywords
     (`single room pg durgapur`, `single room pg in durgapur city centre`, `single seater pg
     durgapur`, `private room pg durgapur`, `single occupancy pg durgapur`, `ac single room pg
     durgapur`…). Rationale: the AC single is the INR 12,000 product and single-room queries
     were landing on generic pages (5 clicks / INR 150 / 0 leads in 28d).
   - **City Centre Durgapur** (199773672149) → `/pg-city-centre-durgapur`, 11 keywords — the
     best historical cluster, previously spread across three groups on generic pages.
   - **Hostel Fees Durgapur** (198808196286) → `/durgapur-hostel-fees`, 11 fee/price keywords.
     Historical 25% CVR on fee queries; the one fee keyword had been sitting inert in Hostel
     Durgapur with 0 impressions.
   All RSAs quote the confirmed tariff (AC single 12,000 · AC double 9,500 · non-AC from
   11,000 · four sharing from 6,000).
5. **8 keywords moved** (removed from the old group after the new ad went live, so no gap):
   from PG Durgapur — `pg in durgapur city centre`, `pg in city centre durgapur`, `paying guest
   durgapur city centre`, `girls pg in bidhannagar durgapur`; from Hostel Durgapur — `girls
   hostel in durgapur city centre`, `hostel in durgapur city centre`, `hostel durgapur fees`;
   from Room Rent — `single room rent in durgapur`. Room Rent was otherwise left intact: it is
   the best group (10 leads / INR 1,482 in 28d).

6. **Budget INR 150 → 220/day** (= INR 6,690/month + GST ≈ 7,890, inside the INR 8,000 cap
   the owners committed to). Note: until the payment cadence is fixed this only drains the
   prepaid balance faster — the top-up size has to follow.

### Landing page map (live 2026-09-11)

| Ad ID | Ad group | Final URL |
|---|---|---|
| 801316412319 | PG Durgapur | `/pg-durgapur` |
| 801316406568 | Hostel Durgapur | `/girls-hostel-durgapur` |
| 801431863814 | Room Rent Durgapur | `/room-rent-durgapur` |
| 801431074463 | Coaching Proximity | `/hostel-near-coaching-durgapur` |
| 824321139076 | Single Room PG Durgapur | `/single-room-pg-durgapur` |
| 824406625613 | City Centre Durgapur | `/pg-city-centre-durgapur` |
| 824280701700 | Hostel Fees Durgapur | `/durgapur-hostel-fees` |

`/locations` remains unassigned (no property in Benachity/Sepco/Fuljhore; page serves the
long tail honestly).

### Baseline to measure the changes against

**Post-LP 28d: 16 leads (6 calls + 10 WhatsApp) · real CPA 234 · site-visit CPC 33.5 ·
IS 28.1% · lost-IS-rank 58.9% · lost-IS-budget 13.1% · 17 serving days.**
Re-read around **2026-10-09**. If the payment fix lands, expect serving days → 28 first;
judge the ad-group changes on site-visit CPC and lost-IS-rank, not on clicks.

### Open items

- Payment cadence (INR 8,000/month single top-up or autopay) — owner.
- Google Business Profile: still "Add website" / possibly unclaimed (from July). 231 of this
  month's clicks went to that listing.
- MCP `add_geo_targets` docstring says "West Bengal=20457" — wrong, that is Gujarat. West
  Bengal is **20472** (Jharkhand 21336, Bihar 20455, Odisha 20465). Fix in
  `google_ads_server.py` before anyone uses it.
- MCP has no tool for keyword pause (only remove), conversion-action settings, or
  `geo_target_type_setting`.
- **Bidding baseline reset on 2026-09-11** (WhatsApp primary + budget 220 + 3 new ad groups
  on the same day). Expect a Max Conversions learning period; don't judge CPA for 2–3 weeks.

---

## ⚠️ Status: audited and changed 2026-07-22

**Everything below the "Live Campaign Structure" heading describes the 21 Mar build and is
partly stale.** Read this section first. Corrections to the old text are called out inline.

### What was actually wrong (90d audit, 2026-07-22)

The account was **not** leaking money. It was capped.

| Metric (live campaign, 90d) | Value |
|---|---|
| Spend | INR 10,276.80 |
| Clicks / Impressions | 504 / 3,547 |
| CTR | 14.21% (excellent) |
| CPC | INR 20.39 |
| Conversions | 16 (all phone calls) |
| CPA | INR 642.30 |
| Search impression share | 41.0% |
| **Lost IS to rank** | **42.5%** |
| Lost IS to budget | 16.5% |

**Rank, not budget, was the ceiling** — ~5,100 impressions per 90d unreachable at any spend.
Cause: **Landing Page Experience was BELOW AVERAGE on 100% of scored keywords**, because all
four ad groups pointed at the bare root `nottingville.space`. Expected CTR was mostly ABOVE
AVERAGE and the ad copy was fine. QS ranged 1-7.

**Negatives were NOT the problem.** Every categorisable waste bucket totalled **INR 300 over
365 days (1.9% of spend)**, most already blocked by the existing negatives. The March negative
work held up. Caveat: `search_term_view` disclosed only **35.9% of spend** (INR 5,811 of
16,209) — Google withholds low-frequency queries, so that 1.9% is 1.9% *of what is visible*.

**The real find:** 5 search terms with `status=NONE` had already produced **6 conversions on
INR 1,047 — CPA INR 174 vs the account average of INR 642**, purely by accident of phrase
matching. They were never keywords.

**Geo truth:** City Centre = 66 clicks / 6 conv / **9.1% CVR** (account avg 2.39%), and
Bidhannagar is the *same township*, not a separate area — all four addresses sit there.
Benachity + Sepco + Fuljhore + Muchipara combined = **10 clicks, 0 conversions, INR 245**, and
we have no property in any of them. Do not build geo pages for those.

**Weekends convert best**: Sun CPA 452 / Sat 495 / Fri 520 vs Mon 1,298 / Wed 1,173. This is the
inverse of the generic B2B dayparting advice — do not cut weekend spend on this account.

**Mobile is ~99% of everything**: 3,465 of 3,547 impressions, 15 of 16 conversions.

### Changes applied 2026-07-22

1. **4 RSAs repointed** off the bare root to matched landing pages (see map below).
2. **5 proven-converting keywords added** (PHRASE):
   `pg in city centre durgapur` (2 conv, CPA 82) · `durgapur pg for girls` · `girls pg in
   bidhannagar durgapur` → **PG Durgapur**;
   `girls hostel in durgapur` · `durgapur hostel` → **Hostel Durgapur**.
   Only the proven 5 — adding the 10 high-traffic non-converters would fragment thin data.
3. **5 campaign negatives added** (PHRASE): `low price` (the only one still actively bleeding,
   INR 111/90d), `youth hostel`, `hourly`, `olx`, `2nd home`.
   Campaign negatives 81 → 86. Active keywords → 47.

**Deliberately NOT changed:** `Nottingville - WhatsApp Click` stays `primary_for_goal = False`.
Owner decision — phone call is the more valuable action, WhatsApp second. Accepted tradeoff:
Smart Bidding optimises on ~16 calls/90d and ignores ~6 WhatsApp leads. Do not propose flipping
it. (Value-based bidding weighting calls higher needs 15+ conv/month; we have ~5.)
> **Reversed 2026-09-11** — post-LP WhatsApp became 60% of leads; see the section above.

### Landing page map (live 2026-07-22)

| Ad ID | Ad group | Final URL |
|---|---|---|
| 801316412319 | PG Durgapur | `/pg-durgapur` |
| 801316406568 | Hostel Durgapur | `/girls-hostel-durgapur` |
| 801431863814 | Room Rent Durgapur | `/room-rent-durgapur` |
| 801431074463 | Coaching Proximity | `/hostel-near-coaching-durgapur` |

Four more pages exist and are unassigned to ad groups, available for future campaigns:
`/pg-city-centre-durgapur` (best cluster), `/durgapur-hostel-fees`, `/single-room-pg-durgapur`,
`/locations`. All 8 generated by `build-lp.py`; see `CLAUDE.md` for the system.

### Corrections to the sections below

- **Bidding/budget:** the doc says Manual CPC at INR 100/day per campaign. The account is
  actually on **MAXIMIZE_CONVERSIONS at INR 150/day**. It drifted after March.
- **"Two Campaigns":** `Nottingville — Near Durgapur` is **PAUSED**. Only
  `Nottingville — Durgapur City` (id 23677229903) runs.
- **Pricing:** the doc's "INR 6,000 starting price" is correct but incomplete. Confirmed
  tariff, per person per month, all four meals included: **AC single 12,000 · AC double sharing
  9,500 · non-AC is 500-1,000 below the AC rate for the same occupancy · four sharing from
  6,000** (the true floor, so the "Starting at ₹6,000/Month" RSA headline is accurate).
  Triple sharing rate still unknown.

### Baseline to measure the changes against

**CPA 642 · CTR 14.21% · IS 41.0% · lost-IS-rank 42.5% · LP experience BELOW AVERAGE on 100%
of keywords.** Re-check Quality Score **in 2-4 weeks, not sooner** — QS updates lag and an
early read will show nothing and mislead.

### Open items

- Triple sharing rate (chart says "Call for rate"); confirm rates are per person.
- Whether a mess-only service is sold — 5 mess keywords are live with no page, and
  `mess in durgapur` historically converted at 33%.
- **Google Business Profile has no website linked** ("Add website" showing). Free high-intent
  traffic. Also shows "Own this business?", which suggests it may be unclaimed — check that
  first. Category is "Student dormitory"; "Hostel"/"Women's hostel" may match search better.
- `index.html` still shows "from ₹6,000" with no rate ladder, unlike the new LPs.

---

## Goal
More relevant **calls and WhatsApp conversations** from parents/students searching for hostels near Durgapur coaching centres.

> 2026-07-22: in practice **calls are the whole business** — all 16 tracked conversions in the
> last 90 days were `Nottingville - Phone Call`. Operator confirms calls and good leads from
> the ground, almost no form fills. The landing pages are built call-first accordingly.

## Conversion Tracking (Already Set Up)
| Action | Type | ID | Label |
|---|---|---|---|
| Nottingville - WhatsApp Click | WEBPAGE | 7537471383 | AW-11090833551/RxJuCJffkoocEI_hwqgp |
| Nottingville - Phone Call | WEBPAGE | 7537302208 | AW-11090833551/3bdACMC1iIocEI_hwqgp |
| Calls from ads | AD_CALL | 1057572880 | — |

Both fire via JS event delegation in `index.html` (lines 1210-1227).

---

## Historical Baselines (All-Time, as of 2026-03-21)
| Metric | Value |
|---|---|
| Total spend | INR 16,031 |
| Clicks | 1,282 |
| Impressions | 12,267 |
| Conversions | 35 |
| Avg CPC | INR 12.50 |
| CTR | 10.5% |
| CVR | 2.73% |
| CPA | INR 458 |

### Top Performing Search Terms (Historical, by CVR)
| Search Term | Clicks | Conv | CVR | CPA (INR) |
|---|---|---|---|---|
| mess in durgapur | 3 | 1 | 33% | 39 |
| durgapur hostel fees | 4 | 1 | 25% | 57 |
| pg in durgapur for female | 18 | 2.5 | 13.9% | 104 |
| pg durgapur / pg at durgapur | 16 | 2 | 12.5% | 94 |
| pg in durgapur benachity | 8 | 1 | 12.5% | 100 |
| hostel in durgapur | 19 | 1 | 5.3% | 266 |
| allen durgapur hostel | 36 | 1 | 2.8% | 439 |
| pg in durgapur city centre | 43 | 1 | 2.3% | 512 |

### Wasted Keywords (Historical — now fixed)
| Search Term | Clicks | Conv | Wasted (INR) | Fix Applied |
|---|---|---|---|---|
| pg near me | 30 | 0 | 294 | Negated "near me" |
| allen durgapur hostel fees | 22 | 0 | 308 | Negated |
| girls pg near me | 14 | 0 | 122 | Negated |
| pg in salt lake / greater noida / etc. | 10+ | 0 | 200+ | Geo fixed to Durgapur only |
| **Total historical waste** | | | **~5,400 (34%)** | |

---

## Live Campaign Structure (deployed 2026-03-21)

### Two Campaigns — Split by Geography

| Campaign | ID | Geo | Budget | Bidding | Status |
|---|---|---|---|---|---|
| Nottingville — Durgapur City | 23677229903 | Durgapur city (ID 9040193) | INR 100/day | Manual CPC | ENABLED |
| Nottingville — Near Durgapur | 23671816026 | 40km radius, Durgapur city excluded | INR 100/day | Manual CPC | ENABLED |

**Total daily budget:** INR 200 (~INR 6,000/month)
**Networks:** Google Search only (no search partners, no Display)
**Ad Schedule:** 24/7 (no restrictions — budget is self-limiting at INR 100/day)
**Geo setting:** "Presence" only — NOT "Presence or interest"

### Why Two Campaigns
- **Durgapur City:** Captures local searches from students/parents already in Durgapur
- **Near Durgapur (40km radius excl. city):** Captures parents in Asansol, Bardhaman, nearby towns searching for Durgapur hostels
- Separate budgets prevent one geo from eating the other's spend
- Allows different bid adjustments per geo as data comes in

### Why 24/7 Schedule (No Dayparting)
- At INR 100/day per campaign (~7 clicks/day), budget is the limiter, not hours
- Indian parents in tier-2 cities browse late on mobile (10 PM–midnight)
- Sunday evenings are prime research time — restricting wastes opportunities
- Google paces the budget naturally; no risk of late-night waste at this budget level

---

## Ad Groups (4 per campaign, 8 total)

All ad groups: CPC bid INR 15, PHRASE match keywords.

### Ad Group 1: PG Durgapur
**Theme:** Core PG/paying guest queries with Durgapur specificity.

**Keywords (PHRASE match):**
```
pg in durgapur
paying guest in durgapur
pg durgapur for female
girls pg in durgapur
pg in durgapur city centre
pg in durgapur benachity
paying guest durgapur city centre
ladies pg durgapur
women pg durgapur
mess in durgapur
ladies mess durgapur
girls mess durgapur
mess for girls durgapur
mess durgapur
```

**RSA Headlines:**
1. PG in Durgapur for Girls (pin pos 1)
2. 60 Beds — AC & Non-AC Rooms
3. 4 Meals/Day Included
4. 24/7 CCTV + Women Wardens
5. Safe PG for Girl Students
6. Run by Mothers, for Daughters
7. WhatsApp Us — Quick Reply
8. Sarojini Naidu Path Location
9. Admissions Open 2026-27
10. Trusted by 60+ Families
11. Nottingville Girls Hostel (pin pos 1)
12. Book a Visit Today
13. Daily Attendance + Curfew
14. Near Top Coaching Centres
15. Call Now for Availability

**RSA Descriptions:**
1. Safe girls PG in Durgapur. 4 meals/day, AC rooms, 24/7 CCTV. WhatsApp now!
2. Run by 3 mothers for your daughter's safety. Near Adhyayan, Aakash, Allen & PW.
3. 60-bed hostel with daily attendance, wardens & medical support. Admissions open.
4. Breakfast, lunch, snacks & dinner included. Gate closes 7 PM. Visit us today.

### Ad Group 2: Hostel Durgapur
**Theme:** Girls hostel queries.

**Keywords (PHRASE match):**
```
girls hostel durgapur
ladies hostel durgapur
hostel in durgapur
hostel in durgapur city centre
best hostel in durgapur
women hostel durgapur
girls hostel in durgapur city centre
hostel durgapur fees
```

**RSA Headlines:**
1. Girls Hostel in Durgapur (pin pos 1)
2. Nottingville Girls Hostel (pin pos 1)
3. 4 Home-Cooked Meals Daily
4. 24/7 CCTV + Daily Attendance
5. AC & Non-AC Rooms Available
6. 7 PM Curfew — Real Safety
7. Run by Mothers, for Daughters
8. Medical Support On-Site
9. WhatsApp for Quick Enquiry
10. 60+ Girls Already Living Here
11. Near All Coaching Centres
12. Admissions Open Now
13. Call Now — Speak to Warden
14. Visit Our 4 Locations
15. Expanding to 100 Beds

**RSA Descriptions:**
1. Not just a hostel — a second home. 24/7 CCTV, wardens, 7 PM curfew, 4 meals/day.
2. Run by 3 mothers who treat every girl like their own daughter. Visit & see yourself.
3. Girls hostel in Durgapur with breakfast, lunch, snacks & dinner. AC + Non-AC rooms.
4. Safe hostel near Adhyayan, Aakash, Allen & PW coaching centres. Call today!

### Ad Group 3: Coaching Proximity
**Theme:** Parents searching for hostels near specific coaching institutes.

**Keywords (PHRASE match):**
```
allen durgapur hostel
hostel near adhyayan durgapur
hostel near aakash durgapur
hostel near physics wallah durgapur
coaching hostel durgapur
hostel for neet students durgapur
hostel for jee students durgapur
student hostel durgapur
hostel near coaching durgapur
```

**RSA Headlines:**
1. Hostel Near Coaching Centres (pin pos 1)
2. Walk to Adhyayan & Aakash
3. For NEET & JEE Students
4. 4 Meals + AC Rooms Included
5. Girls Hostel — Durgapur
6. Focus on Studies, Not Chores
7. Near Allen & PW Durgapur
8. Daily Attendance Register
9. Mothers Running the Hostel
10. WhatsApp for Availability
11. Safe for Your Daughter
12. 60 Beds — Filling Fast
13. Admissions Open 2026-27
14. Nottingville Girls Hostel
15. Call Now for Room Tour

**RSA Descriptions:**
1. Girls hostel steps from Durgapur's top coaching centres. 4 meals, CCTV, wardens.
2. Your daughter prepares for NEET/JEE while we handle safety, food & daily needs.
3. Near Adhyayan, Aakash, Allen & Physics Wallah. AC rooms, 4 meals, 7 PM curfew.
4. 60 girls already trust us. Daily attendance, medical support. Book before full.

### Ad Group 4: Room Rent Durgapur
**Theme:** Accommodation/room rent queries — high volume (450+/mo), mixed intent. Monitor search terms closely for flat-seeker leakage.

**Keywords (PHRASE match):**
```
room rent durgapur
room rent in durgapur
durgapur room rent
room rent in durgapur west bengal
room rent in durgapur city centre
room rent in durgapur benachity
room rent in bidhannagar durgapur
room rent durgapur for female
room rent for girls durgapur
single room rent in durgapur
```

**RSA Headlines:**
1. Room Rent in Durgapur (pin pos 1)
2. Nottingville Girls Hostel (pin pos 1)
3. Girls Rooms — AC & Non-AC
4. 4 Meals/Day Included
5. Starting at ₹6,000/Month
6. 24/7 CCTV + Women Wardens
7. Run by Mothers, for Daughters
8. Near Top Coaching Centres
9. WhatsApp for Availability
10. 60+ Girls Already Here
11. Daily Attendance + Curfew
12. 4 Locations in Durgapur
13. Admissions Open 2026-27
14. Call Now — Visit Today
15. Safe Rooms for Girl Students

**RSA Descriptions:**
1. Girls room rent in Durgapur with 4 meals/day, AC options, 24/7 CCTV. WhatsApp now!
2. Not just a room — a safe home. Wardens, 7 PM curfew, daily attendance. Visit today.
3. Run by 3 mothers. Near Adhyayan, Aakash, Allen & PW coaching. Admissions open.
4. 60-bed hostel with breakfast, lunch, snacks & dinner. AC + Non-AC. Book before full.

---

## Negative Keywords

### Campaign-Level (Phrase Match) — Applied to BOTH campaigns (77 total)
```
# Boys/men
boy, boys, male, gents, men, boys hostel, gents hostel, men hostel

# Other cities
kolkata, calcutta, delhi, mumbai, pune, bangalore, chennai, hyderabad,
jaipur, lucknow, patna, siliguri, howrah, ranchi, varanasi, coimbatore,
indore, bhubaneswar, kota, noida, gurgaon, chandigarh

# Hotels/travel
hotel, resort, oyo, airbnb, booking, dharamshala, guest house booking

# Jobs
job, jobs, career, salary, vacancy, warden job, cook, staff, hiring

# DIY/informational
how to start, hostel business, hostel management, hostel rules, hostel life vlog

# Free/government
free hostel, government hostel, scholarship hostel

# "Near me" (leaks to all-India)
near me, nearby, near by

# Real estate
real estate, scottish

# Flat-seekers (protects Room Rent ad group)
flat, apartment, 2 bhk, 3 bhk, family, couple, bachelor,
office, shop, commercial, warehouse, godown

# Budget searchers (below our INR 6,000 starting price)
under 1500, under 2000, under 3000

# Coaching fee queries (want coaching fees, not hostel)
allen hostel fees, allen coaching fees, aakash fees
```

---

## Geo Targeting

### Campaign 1: Durgapur + 30km
- **Target:** 30km radius around Durgapur (lat 23.5204, lng 87.3119)
- **Coverage:** Durgapur, Bamunara, Kanksa, Andal, Panagarh, Asansol, Raniganj, Kulti
- **Setting:** Presence only

### Campaign 2: Near Durgapur
- **Target:** 100km radius around Durgapur (lat 23.5204, lng 87.3119)
- **Exclude (9 locations within ~30km):** Durgapur city (9040193), Durgapur sub-district (9184076), Bamunara (9298472), Kanksa (9298972), Andal (9298966), Asansol (9298469), Panagarh (9299607), Raniganj (9298963), Kulti (9300537)
- **Setting:** Presence only
- **Rationale:** People within 30km of Durgapur are close enough to know the area — the real audience is parents 30-100km away (Bardhaman ~55km, Bankura ~65km, Bishnupur ~80km, Bolpur ~90km) whose kids need accommodation
- **Note:** Barjora (8km), Sonamukhi (23km), Bahula (24km) only have postal code IDs — no city-level exclusion possible, but negligible search volume

## Ad Schedule
**None (24/7).** Budget is the natural limiter at INR 100/day per campaign. See "Why 24/7 Schedule" above.

## Extensions (linked to both campaigns)

### Call Assets
- Phone 1: +91 84361 50885 (primary for ads)
- Phone 2: +91 79089 78959

### Sitelinks
| Text | URL | Description 1 | Description 2 |
|---|---|---|---|
| See Photos | nottingville.space#story | View hostel rooms and facilities | Photos of AC & Non-AC rooms |
| Our Locations | nottingville.space#locations | 4 locations in Durgapur | Sarojini Naidu Path & more |
| Safety Features | nottingville.space#why | CCTV, wardens, curfew | Daily attendance register |
| WhatsApp Us | nottingville.space#contact | Quick reply on WhatsApp | Talk to us directly |

### Callouts
```
4 Meals/Day | 24/7 CCTV | AC & Non-AC | Run by Mothers | Near Coaching Centres | Medical Support
```

---

## Budget & Bidding Progression

| Phase | When | Strategy | Budget |
|---|---|---|---|
| **Launch (current)** | Day 1-30 | Manual CPC (INR 15 bid) | INR 200/day total |
| Optimize | After 15+ conv | Maximize Conversions | INR 200/day |
| Scale | After 30+ conv, stable CPA | Target CPA (INR 200-400) | INR 400/day |

**Expected performance (based on historical + keyword planner):**
- Avg CPC: INR 12-15
- Monthly clicks: 400-500 (at INR 200/day)
- CVR: 3-5% (with tighter targeting)
- Expected leads/month: 12-25
- Expected CPA: INR 200-400

---

## Keyword Planner Data (Durgapur geo, March 2026)

### Market Volume by Cluster
| Cluster | Monthly Searches | In Campaigns? |
|---|---|---|
| hostel/hostel in durgapur | 340+ | ✓ |
| pg/paying guest durgapur | 220+ | ✓ |
| room rent durgapur | 450+ | ✓ (added) |
| ladies hostel durgapur | 70 | ✓ |
| mess in durgapur | ~30 | ✓ (added) |
| accommodation durgapur | 50 | Not yet |
| coaching-specific (allen, adhyayan) | 50-80 | ✓ |
| college-specific (NIT, NSHM) | 20-40 | Not yet |
| **durgapur hotels (NEGATIVE)** | **1,600** | **Negated** |

### Future Keywords to Test
```
# Accommodation (50/mo)
accommodation durgapur

# College proximity (20/mo each)
pg near nit durgapur
pg near nshm durgapur
hostel near nit durgapur

# Locality-specific (10-20/mo each)
room rent near mission hospital durgapur
room rent in durgapur muchipara
```

---

## Old Campaigns (Reference — all paused)
| Campaign | ID | Status | Notes |
|---|---|---|---|
| EK \| Theme \| Pg / Hostel in Durgapur \| 10-Feb | 19668768710 | PAUSED | Historical data reference |
| Student Dormitory near You | 19660354302 | PAUSED | Can remove |
| Video Non-skippable - 2023-02-23 | 19728405286 | PAUSED | Can remove |
| Video Custom - 2023-02-24 | 19732070300 | ENABLED | **Pause manually** — API can't mutate video campaigns |

---

## Weekly Check-In Process
Use `/google-ads-weekly` skill or run manually:

1. **Performance** — Pull last 7 days vs previous 7 days (clicks, conv, CPA, spend)
2. **Search terms** — Flag irrelevant queries, add negatives
3. **Budget** — Check if capped (spend >= 95% of budget)
4. **Conversions** — Verify WhatsApp + phone tracking still firing
5. **Quality Score** — Check keywords with QS < 5
6. **Room Rent monitoring** — Watch for flat-seeker/family search terms in Room Rent ad group
7. **Geo split** — Compare City vs Near Durgapur performance
8. **Action items** — Pause losers, raise bids on winners, add new keywords from search terms

---

## Key Learnings
1. **Durgapur-specific keywords convert, "near me" doesn't** — always include city name
2. **Coaching proximity keywords have highest CVR** (5.3-6.3%) — invest here
3. **CPCs are dirt cheap** (INR 12-15) — budget goes far
4. **"Female" qualifier boosts CVR** — "pg in durgapur for female" had 13.9% CVR
5. **Fees-related queries convert** — "durgapur hostel fees" had 25% CVR
6. **"Mess" queries convert extremely well** — "mess in durgapur" had 33% CVR (1 conv from 3 clicks)
7. **Phrase match > Broad match** — broad match leaked to irrelevant "near me" traffic
8. **Presence-only geo targeting is critical** — "Presence or Interest" leaked to all-India
9. **Room rent is the biggest search volume cluster** (450+/mo) — needs monitoring for mixed intent
10. **Prices start at INR 6,000/month** — negate budget searchers (under 3000, under 2000, under 1500)

---

## MCP Server Fixes (applied 2026-03-21)
- `containsEuPoliticalAdvertising` enum field required on campaign creation (API v20)
- `geoTargetTypeSetting` (Presence only) set automatically on new campaigns
- `add_geo_targets` now supports `negative=True` for geo exclusions
- New `add_proximity_target` tool for radius targeting (lat, lng, radius_km)
