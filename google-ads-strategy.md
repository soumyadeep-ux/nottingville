# Nottingville — Google Ads Strategy

**Account ID:** 5886623748
**Currency:** INR | **Timezone:** Asia/Calcutta
**Google Ads Tag:** AW-11090833551
**MCC:** 8952449784 (Ekamoira Marketing)
**MCP Server:** `/Users/soumyadeepmukherjee/Documents/mcp-google-ads/google_ads_server.py`

---

## Goal
More relevant **calls and WhatsApp conversations** from parents/students searching for hostels near Durgapur coaching centres.

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
