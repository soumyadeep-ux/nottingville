#!/usr/bin/env python3
"""
Nottingville — landing page generator.

Generates the Google Ads landing pages from one config each. The SITE stays a
plain static folder (no deploy-time build): run this once, commit the .html
output, deploy as usual.

    python3 build-lp.py

Every fact used below is verified against CLAUDE.md, the live index.html, or the
Google Business Profile. Nothing here is invented. Where a number is not known
(exact AC/non-AC tariff), the page asks the visitor to call rather than guessing.
"""

import hashlib
import html
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
SITE = "https://nottingville.space"


def asset_url(name):
    """Cache-busting URL for a mutable asset.

    `_headers` serves /assets/* as `max-age=31536000, immutable` on stable
    filenames. `immutable` tells the browser not even to revalidate, so without
    a version in the URL an edit to lp.css/lp.js can never reach anyone who has
    already loaded a landing page — they would hold the old copy for a year.
    Hashing the content means the URL changes exactly when the file does, which
    keeps the long immutable cache correct instead of dangerous.
    """
    digest = hashlib.md5((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]
    return f"/assets/{name}?v={digest}"


CSS_URL = asset_url("lp.css")
JS_URL = asset_url("lp.js")

# ── Verified constants ────────────────────────────────────────────────────────
WA_NUMBER = "917908978959"          # matches index.html + Google Ads call asset
TEL_PRIMARY = "+917908978959"
TEL_ALL = [("+917908978959", "+91 79089 78959"),
           ("+919126660502", "+91 91266 60502"),
           ("+918436150885", "+91 84361 50885")]
# Owner-confirmed 2026-07-22. Non-AC is Rs 500-1,000 below the AC rate for the
# same occupancy. Triple and four-bedded rates were not supplied, so they read
# "Call for rate" rather than being guessed.
PRICE_AC_SINGLE = "12,000"
PRICE_AC_DOUBLE = "9,500"
PRICE_FROM = "6,000"                  # four sharing — the true entry price
# (room, ac, non_ac, span) — span=True renders one figure across both columns,
# used where the owner gave a single rate rather than an AC/Non-AC split.
TARIFF = [
    ("Single occupancy", "Rs 12,000", "Rs 11,000 &ndash; 11,500", False),
    ("Double sharing",   "Rs 9,500",  "Rs 8,500 &ndash; 9,000", False),
    ("Triple sharing",   "Call for rate", "", True),
    ("Four bedded",      "From Rs 6,000", "", True),
]
RATING, REVIEW_COUNT = "4.6", "17"   # Google Business Profile, verified

MEALS = [
    ("Morning", "Breakfast", "Rotating daily menu: Luchi, Puri, Roti, Idli or Maggi. "
     "A proper hearty start, never skipped.", "Rotating Menu"),
    ("Afternoon", "Lunch", "Rice, dal and sides. Non-vegetarian six days a week: "
     "chicken, fish and egg. One vegetarian day.", "Non-veg 6 Days"),
    ("Evening", "Snacks &amp; Tea", "Evening refreshments with tea, timed to recharge "
     "her through the long study hours.", "Daily"),
    ("Night", "Dinner", "A comforting home-style dinner every night. Fresh, hygienic, "
     "cooked with genuine care.", "Home Cooked"),
]

FACILITIES = [
    ("4 meals every day", "Breakfast, lunch, evening snacks with tea, and dinner. All included in the rent."),
    ("Non-veg six days a week", "Chicken, fish and egg through the week. One vegetarian day."),
    ("Aquaguard drinking water", "Purified drinking water on every floor."),
    ("Free WiFi", "Included, so study material and online classes never stall."),
    ("24x7 CCTV and women wardens", "Cameras across common areas, with wardens on site around the clock."),
    ("7 PM curfew, daily attendance", "The gate closes at 7 PM and opens at 6 AM. Attendance is registered daily."),
    ("AC and Non-AC rooms", "60 beds today, expanding to 100. Choose the room that suits your budget."),
    ("Medical support on site", "Help is arranged immediately if she falls ill, at any hour."),
    ("Run by three mothers", "Not a landlord and not a chain. Three mothers who raise their own daughters here."),
]

LOCATIONS = [
    ("10/1 Sarojini Naidu Path", "Non-Company Housing Estate, City Center, Durgapur 713216"),
    ("10/3 Sarojini Naidu Path", "Non-Company Housing Estate, City Center, Durgapur"),
    ("D45 Uday Shankar", "City Center, Durgapur"),
    ("55 Tarashankar", "City Center, Durgapur"),
]

REVIEWS = [
    ("Home like Food, Aquaguard water available. Free wifi Hygeine maintained.", "Google review"),
    ("I feel here like my home. All aunties treated us like their own children.", "Google review"),
    ("Very good behaviour and well organised", "Google review"),
]

COACHING = [("Adhyayan", "Durgapur"), ("Physics Wallah", "Durgapur"),
            ("Aakash", "Institute"), ("Allen", "Career Institute")]
EXAMS = ["NEET UG", "JEE Main", "JEE Advanced", "BITSAT", "CUET"]

NAV_PAGES = [
    ("pg-durgapur", "PG in Durgapur"),
    ("girls-hostel-durgapur", "Girls Hostel"),
    ("room-rent-durgapur", "Room Rent"),
    ("durgapur-hostel-fees", "Fees"),
    ("locations", "Locations"),
]


# ── Page configs ──────────────────────────────────────────────────────────────
# `evidence` is a build-time note only; it does not render.
PAGES = [
{
 "slug": "pg-durgapur",
 "evidence": "PG Durgapur ad group — 216 clicks, 8 conv (best performing ad group)",
 "kw": "PG in Durgapur",
 "title": "PG in Durgapur for Girls — 4 Meals Daily | Nottingville",
 "desc": ("Girls PG in Durgapur. AC double sharing Rs 9,500, single Rs 12,000, "
          "non-veg six days a week, AC and Non-AC rooms, 24x7 CCTV. Rated 4.6 on Google. Call now."),
 "keywords": "pg in durgapur, girls pg in durgapur, paying guest in durgapur, pg durgapur for female, ladies pg durgapur, women pg durgapur",
 "badge": "Paying Guest &middot; Durgapur",
 "h1": 'PG in Durgapur <em>where the food tastes like home</em>',
 "sub": ("A girls-only paying guest accommodation run by three mothers. Four meals a day, "
         "non-vegetarian six days a week, and a warden who notices when she skips dinner."),
 "lede": ("If you are looking for a <strong>PG in Durgapur for girls</strong>, the question that "
          "actually decides the year is not the room. It is the food. Nottingville serves "
          "<strong>four home-cooked meals every single day</strong>, with non-vegetarian on six of "
          "the seven days, and all of it is included in your rent. There is no separate mess bill "
          "and no evening scramble for a tiffin service."),
 "points": [
   "Four meals daily: breakfast, lunch, evening snacks with tea, and dinner",
   "Non-vegetarian six days a week: chicken, fish and egg. One vegetarian day",
   "AC double sharing Rs 9,500, single Rs 12,000. All meals included, no mess charge",
   "AC and Non-AC rooms across four addresses in City Center, Durgapur",
   "24x7 CCTV, women wardens, 7 PM curfew and a daily attendance register",
 ],
 "blocks": ["food", "review", "tariff", "pillars", "facilities", "locations", "faq"],
 "faq": [
   ("Is food included in the PG rent in Durgapur?",
    "Yes. All four meals are included in the monthly rent at Nottingville. Breakfast, lunch, "
    "evening snacks with tea and dinner are covered, so there is no separate mess bill to budget for."),
   ("Is non-vegetarian food served at the PG?",
    "Yes. Lunch is non-vegetarian six days a week, rotating through chicken, fish and egg, with "
    "one vegetarian day. Breakfast rotates between Luchi, Puri, Roti, Idli and Maggi."),
   ("What does a PG in Durgapur cost at Nottingville?",
    "AC single occupancy is Rs 12,000 and AC double sharing is Rs 9,500, both including all four "
    "meals. Non-AC rooms are Rs 500 to Rs 1,000 less. Four sharing starts at Rs 6,000, which is "
    "our lowest rate. Call or WhatsApp us for triple sharing."),
   ("Is the PG only for girls?",
    "Yes. Nottingville is a girls-only paying guest accommodation. It is run by three mothers, "
    "with women wardens on site, a 7 PM curfew and a daily attendance register."),
 ],
 "wa": "Hi, I'd like to enquire about a PG in Durgapur at Nottingville.",
},
{
 "slug": "girls-hostel-durgapur",
 "evidence": "Hostel Durgapur ad group — 97 clicks, 3 conv; 'girls hostel in durgapur' 21 clicks 1 conv unowned",
 "kw": "girls hostel in Durgapur",
 "title": "Girls Hostel in Durgapur — 4 Meals a Day | Nottingville",
 "desc": ("Girls hostel in Durgapur rated 4.6 on Google. Four home-cooked meals daily, non-veg six "
          "days a week, 24x7 CCTV, women wardens, 7 PM curfew. See full room rates. Call now."),
 "keywords": "girls hostel in durgapur, girls hostel durgapur, ladies hostel durgapur, women hostel durgapur, hostel in durgapur, durgapur girls hostel",
 "badge": "Girls Hostel &middot; Durgapur",
 "h1": 'A girls hostel in Durgapur <em>run by mothers</em>',
 "sub": ("Four meals a day, non-vegetarian six days a week, 24x7 CCTV and a warden who knows "
         "every girl by name. Rated 4.6 by families on Google."),
 "lede": ("Most searches for a <strong>girls hostel in Durgapur</strong> end with the same two "
          "worries: is she safe, and is she eating properly. Nottingville answers both. "
          "<strong>Four home-cooked meals arrive every day</strong>, non-vegetarian on six of them, "
          "and the gate closes at 7 PM with attendance registered daily. It is run by three mothers "
          "who raise their own daughters in the same building."),
 "points": [
   "Four home-cooked meals daily, all included in the rent",
   "Non-vegetarian six days a week: chicken, fish and egg",
   "24x7 CCTV, women wardens on site, medical support at any hour",
   "Gate closes 7 PM and opens 6 AM, with a daily attendance register",
   "60 beds across four addresses in City Center, expanding to 100",
 ],
 "blocks": ["food", "review", "tariff", "pillars", "facilities", "locations", "coaching", "faq"],
 "faq": [
   ("What food is served at your girls hostel in Durgapur?",
    "Four meals a day. Breakfast rotates between Luchi, Puri, Roti, Idli and Maggi. Lunch is rice, "
    "dal and sides with non-vegetarian six days a week. Evening brings snacks and tea, and dinner "
    "is home-style. Everything is included in the rent."),
   ("How safe is the hostel?",
    "There is 24x7 CCTV across common areas, women wardens on site, a daily attendance register, "
    "and the gate closes at 7 PM and opens at 6 AM. Medical support is arranged immediately at any hour."),
   ("What does the girls hostel in Durgapur cost?",
    "AC single occupancy is Rs 12,000 and AC double sharing is Rs 9,500, with all four meals "
    "included. Non-AC is Rs 500 to Rs 1,000 less, and four sharing starts at Rs 6,000. Call or "
    "WhatsApp for triple sharing."),
   ("Where is the hostel located?",
    "Four addresses in City Center, Durgapur: 10/1 and 10/3 Sarojini Naidu Path, D45 Uday Shankar "
    "and 55 Tarashankar. All are within the City Center and Bidhannagar area."),
 ],
 "wa": "Hi, I'd like to enquire about the girls hostel in Durgapur.",
},
{
 "slug": "room-rent-durgapur",
 "evidence": "Room Rent Durgapur ad group — 181 clicks, 5 conv",
 "kw": "room rent in Durgapur",
 "title": "Room Rent in Durgapur for Girls — Meals Included | Nottingville",
 "desc": ("Room rent in Durgapur for girls with all four meals included. Double sharing from "
          "Rs 8,500, AC and Non-AC rooms, Aquaguard water, free WiFi, 24x7 CCTV. Rated 4.6."),
 "keywords": "room rent in durgapur, room rent durgapur, durgapur room rent, single room rent in durgapur, room rent for girls durgapur, room rent durgapur for female",
 "badge": "Room Rent &middot; Durgapur",
 "h1": 'Room rent in Durgapur, <em>with all four meals included</em>',
 "sub": ("A rented room usually means finding your own food. Here it does not. Rent starts at "
         "Rs 8,500 for non-AC double sharing, and every meal is already covered."),
 "lede": ("Compare <strong>room rent in Durgapur</strong> carefully and the cheap option rarely stays "
          "cheap. A bare room means a mess subscription, a tiffin service, or cooking after a full "
          "day of classes. At Nottingville <strong>every room rate already includes all four "
          "meals</strong>, purified drinking water and WiFi, so the number you are quoted is the "
          "number you actually pay. Double sharing starts at Rs 8,500."),
 "points": [
   "Double sharing from Rs 8,500, single from Rs 11,000, with four meals included",
   "No separate mess bill, no tiffin subscription, no cooking after class",
   "Non-vegetarian six days a week: chicken, fish and egg",
   "AC and Non-AC rooms, Aquaguard drinking water and free WiFi",
   "Girls only, with 24x7 CCTV, women wardens and a 7 PM curfew",
 ],
 "blocks": ["food", "review", "tariff", "facilities", "locations", "faq"],
 "faq": [
   ("What is the room rent in Durgapur at Nottingville?",
    "Non-AC double sharing starts at Rs 8,500 and AC double sharing is Rs 9,500. Single occupancy "
    "is Rs 12,000 with AC. Every rate already includes all four meals a day. Four sharing starts "
    "at Rs 6,000, our lowest rate."),
   ("Is food extra on top of the room rent?",
    "No. Four meals a day are included in the rent. There is no separate mess charge, which is the "
    "main reason a room here works out cheaper than a bare room plus a mess subscription."),
   ("Do you rent single rooms?",
    "Room types vary across our four addresses and availability changes through the year. Tell us "
    "what you need on WhatsApp and we will tell you honestly what is free right now."),
   ("Is the room rent only for girls?",
    "Yes. Nottingville accommodates girls and women only."),
 ],
 "wa": "Hi, I'd like to enquire about room rent in Durgapur at Nottingville.",
},
{
 "slug": "pg-city-centre-durgapur",
 "evidence": "STRONGEST CLUSTER — City Centre 66 clicks 6 conv (9.1% CVR) + Bidhannagar 12 clicks 1 conv",
 "kw": "PG in City Centre Durgapur",
 "title": "PG in City Centre Durgapur (Bidhannagar) — 4 Meals | Nottingville",
 "desc": ("Girls PG and hostel in City Centre Durgapur, Bidhannagar. All four addresses are in City "
          "Center. Four meals daily, non-veg six days a week. Full room rates inside. Rated 4.6."),
 "keywords": "pg in city centre durgapur, girls pg in durgapur city centre, girls hostel in durgapur city centre, pg in bidhannagar durgapur, room rent in durgapur city centre, paying guest in durgapur city centre",
 "badge": "City Center &middot; Bidhannagar",
 "h1": 'PG in City Centre Durgapur, <em>all four addresses</em>',
 "sub": ("Every Nottingville address sits inside City Center, Bidhannagar. Four meals a day, "
         "non-vegetarian six days a week, from Rs 8,500 for double sharing."),
 "lede": ("If you are searching for a <strong>PG in City Centre Durgapur</strong>, this is the "
          "straightforward answer: <strong>all four of our addresses are in City Center</strong>, "
          "in the Non-Company Housing Estate and Bidhannagar area. You are not being sent to the "
          "edge of town. And the food is the part families remember: four home-cooked meals daily, "
          "non-vegetarian six days a week, included in the rent."),
 "points": [
   "All four addresses inside City Center, Bidhannagar, Durgapur 713216",
   "10/1 and 10/3 Sarojini Naidu Path, D45 Uday Shankar, 55 Tarashankar",
   "Four meals a day included, non-vegetarian six days a week",
   "Close to the City Center market, transport and coaching centres",
   "AC double sharing Rs 9,500, with 24x7 CCTV, women wardens and a 7 PM curfew",
 ],
 "blocks": ["food", "review", "tariff", "locations", "distances", "facilities", "coaching", "faq"],
 "faq": [
   ("Is Nottingville actually in City Centre Durgapur?",
    "Yes. All four addresses are within City Center, Durgapur 713216: 10/1 and 10/3 Sarojini Naidu "
    "Path in the Non-Company Housing Estate, D45 Uday Shankar and 55 Tarashankar."),
   ("Is City Centre the same as Bidhannagar?",
    "In Durgapur the two names are used for the same area. Our addresses sit in the Bidhannagar "
    "planned township, which locals and Google both refer to as City Center."),
   ("What food do you serve at the City Centre PG?",
    "Four meals daily. Breakfast rotates between Luchi, Puri, Roti, Idli and Maggi. Lunch is "
    "non-vegetarian six days a week with chicken, fish and egg. Evening snacks with tea, then a "
    "home-style dinner. All included in the rent."),
   ("What does a PG in City Centre Durgapur cost?",
    "AC double sharing is Rs 9,500 and AC single occupancy is Rs 12,000, every meal included. "
    "Non-AC is Rs 500 to Rs 1,000 less, and four sharing starts at Rs 6,000."),
 ],
 "wa": "Hi, I'd like to enquire about a PG in City Centre Durgapur.",
},
{
 "slug": "durgapur-hostel-fees",
 "evidence": "Fees/price cluster 10 clicks; historical 'durgapur hostel fees' 25% CVR. Also filters out 'low price'",
 "kw": "Durgapur hostel fees",
 "title": "Girls Hostel &amp; PG Fees in Durgapur — Full Room Rates",
 "desc": ("Girls hostel and PG fees in Durgapur. AC single Rs 12,000, double sharing Rs 9,500, "
          "and no separate mess bill. See exactly what the fee covers. Rated 4.6 on Google."),
 "keywords": "durgapur hostel fees, durgapur girls hostel price, hostel durgapur fees, pg fees durgapur, girls hostel fees in durgapur, hostel rent durgapur",
 "badge": "Fees &middot; What It Includes",
 "h1": 'Girls hostel and PG fees in Durgapur, <em>food included</em>',
 "sub": ("AC single Rs 12,000. AC double sharing Rs 9,500. Every rate covers all four meals. "
         "No separate mess bill, no tiffin subscription, no surprise additions."),
 "lede": ("Comparing <strong>Durgapur hostel fees</strong> is harder than it should be, because most "
          "quotes leave out food. A room at Rs 4,500 with a mess bill on top is not cheaper than "
          "ours. At Nottingville <strong>every rate below already includes all four meals</strong>, "
          "non-vegetarian six days a week, plus purified water and WiFi. That is the whole number."),
 "points": [
   "AC single Rs 12,000, AC double sharing Rs 9,500, all four meals already included",
   "No separate mess charge and no tiffin subscription to add on",
   "Non-vegetarian six days a week: chicken, fish and egg",
   "Aquaguard drinking water and free WiFi included",
   "Final rate depends on AC or Non-AC and the sharing arrangement",
 ],
 "blocks": ["tariff", "food", "review", "facilities", "locations", "faq"],
 "faq": [
   ("What are the hostel fees in Durgapur at Nottingville?",
    "AC single occupancy is Rs 12,000 a month and AC double sharing is Rs 9,500, both including all "
    "four meals. Non-AC rooms are Rs 500 to Rs 1,000 less than the AC rate for the same "
    "occupancy. Four sharing starts at Rs 6,000, which is the lowest rate we offer."),
   ("Is there a separate mess or food charge?",
    "No. Four meals a day are included in the monthly fee. That is breakfast, lunch, evening snacks "
    "with tea, and dinner, with non-vegetarian six days a week."),
   ("Why are your fees higher than a bare room?",
    "Because a bare room is not comparable. Once you add a mess subscription or tiffin service to a "
    "cheaper room, the total is usually higher than ours, and the food is rarely home-cooked. Our "
    "fee is the complete monthly cost."),
   ("What else is included in the fee?",
    "Aquaguard drinking water, free WiFi, 24x7 CCTV, women wardens, a daily attendance register and "
    "medical support arranged at any hour."),
 ],
 "wa": "Hi, I'd like to know the current fees at Nottingville Hostel, Durgapur.",
},
{
 "slug": "single-room-pg-durgapur",
 "evidence": "Single/private room cluster — 10 clicks, 9 terms, entirely unowned",
 "kw": "single room PG in Durgapur",
 "title": "Single Room PG in Durgapur for Girls — Meals Included | Nottingville",
 "desc": ("Single and shared room options at a girls PG in Durgapur City Centre. Four meals a day "
          "included, non-veg six days a week. AC single Rs 12,000, double sharing Rs 9,500."),
 "keywords": "single room pg in durgapur, single room rent in durgapur, single room pg in durgapur city centre, single occupancy pg durgapur, ac pg in durgapur",
 "badge": "Room Options &middot; Durgapur",
 "h1": 'Single room PG in Durgapur, <em>with every meal covered</em>',
 "sub": ("AC and Non-AC options across four City Center addresses. Availability moves through the "
         "year, so ask us what is free right now."),
 "lede": ("A <strong>single room PG in Durgapur</strong> is about wanting quiet and privacy to study. "
          "We have AC and Non-AC options across four addresses in City Center, and availability "
          "genuinely changes through the admission season. What does not change is the food: "
          "<strong>four home-cooked meals a day</strong>, non-vegetarian six days a week, included."),
 "points": [
   "AC and Non-AC rooms, single and shared, across four City Center addresses",
   "60 beds today and expanding to 100, so ask about current availability",
   "Four meals a day included in every room rate, whichever occupancy you pick",
   "Non-vegetarian six days a week: chicken, fish and egg",
   "Quiet study conditions with a 7 PM curfew and daily attendance",
 ],
 "blocks": ["food", "review", "tariff", "facilities", "locations", "faq"],
 "faq": [
   ("Do you have single occupancy rooms?",
    "Room types and availability vary across our four addresses and change through the admission "
    "season. Tell us what you are looking for on WhatsApp and we will tell you honestly what is "
    "free right now rather than making you visit for nothing."),
   ("Are AC rooms available?",
    "Yes, we have both AC and Non-AC rooms. The monthly rate differs between them. Call or WhatsApp "
    "for the current tariff."),
   ("Is food included with a single room?",
    "Yes. All four meals a day are included regardless of the room type you choose, with "
    "non-vegetarian six days a week."),
 ],
 "wa": "Hi, I'd like to ask about single room availability at Nottingville, Durgapur.",
},
{
 "slug": "hostel-near-coaching-durgapur",
 "evidence": "Coaching Proximity ad group — 10 clicks, 0 conv. A bet, but the highest-LTV audience (full-year stays)",
 "kw": "hostel near coaching in Durgapur",
 "title": "Girls Hostel Near Coaching Centres in Durgapur | Nottingville",
 "desc": ("Girls hostel in Durgapur City Centre for NEET and JEE students. Four meals daily so she "
          "never studies hungry, 7 PM curfew, daily attendance. Full room rates inside."),
 "keywords": "hostel near coaching durgapur, allen durgapur hostel, hostel for neet students durgapur, hostel for jee students durgapur, student hostel durgapur, hostel near aakash durgapur, pg near nshm durgapur",
 "badge": "For NEET &amp; JEE Students",
 "h1": 'A hostel near coaching in Durgapur, <em>so she only studies</em>',
 "sub": ("Four meals arrive on time every day. No cooking, no tiffin queue, no skipped dinner "
         "before an exam."),
 "lede": ("A student preparing for NEET or JEE has no spare hours to spend on food. That is the real "
          "argument for a <strong>hostel near coaching in Durgapur</strong>. Nottingville sits in "
          "City Center, close to the coaching belt, and serves <strong>four home-cooked meals a "
          "day</strong> on a fixed schedule, with evening tea timed for the long study stretch."),
 "points": [
   "Four meals daily on a fixed schedule, including evening snacks and tea",
   "Non-vegetarian six days a week, so protein is not an afterthought",
   "In City Center, Durgapur, near the coaching centres and NSHM",
   "7 PM curfew and a daily attendance register, reported to parents",
   "Medical support arranged at any hour, day or night",
 ],
 "blocks": ["food", "coaching", "review", "tariff", "pillars", "facilities", "locations", "faq"],
 "faq": [
   ("Which coaching centres are you near?",
    "We are in City Center, Durgapur, close to the coaching belt including Adhyayan, Physics Wallah, "
    "Aakash and Allen, and near NSHM. Call us and we will tell you the exact travel time from the "
    "address you need."),
   ("Do meal timings suit coaching hours?",
    "Yes. Four meals run on a fixed daily schedule, with evening snacks and tea timed to carry her "
    "through the study hours after class. If class timings clash, speak to the warden."),
   ("Is it suitable for NEET and JEE students?",
    "Yes. Most of our girls are preparing for NEET UG, JEE Main, JEE Advanced, BITSAT or CUET. "
    "The 7 PM curfew and daily attendance exist precisely to protect study time."),
 ],
 "wa": "Hi, I'd like to enquire about a hostel near coaching in Durgapur for a NEET/JEE student.",
},
{
 "slug": "locations",
 "evidence": "Serves the Benachity/Sepco/Fuljhore/Muchipara long tail HONESTLY — we have no property there",
 "kw": "Nottingville locations in Durgapur",
 "title": "Our 4 Locations in City Center, Durgapur | Nottingville",
 "desc": ("All four Nottingville girls hostel addresses are in City Center, Durgapur 713216. See "
          "each address and how far it is from Benachity, Sepco, Muchipara and the station."),
 "keywords": "nottingville durgapur address, girls hostel city center durgapur, hostel near durgapur station, pg near benachity durgapur, hostel bidhannagar durgapur",
 "badge": "Four Addresses &middot; One Area",
 "h1": 'All four addresses, <em>all in City Center</em>',
 "sub": ("We are honest about where we are. Every Nottingville building sits in City Center, "
         "Bidhannagar. If you are looking elsewhere in Durgapur, here is the real distance."),
 "lede": ("People search for a hostel in Benachity, Sepco, Muchipara and Fuljhore, so here is the "
          "straight answer: <strong>all four Nottingville addresses are in City Center, "
          "Bidhannagar</strong>. We do not have a building in those neighbourhoods and we will not "
          "pretend otherwise. If City Center works for your commute, the food and the safety are "
          "worth the trip."),
 "points": [
   "10/1 Sarojini Naidu Path, Non-Company Housing Estate, City Center, Durgapur 713216",
   "10/3 Sarojini Naidu Path, Non-Company Housing Estate, City Center",
   "D45 Uday Shankar, City Center",
   "55 Tarashankar, City Center",
 ],
 "blocks": ["locations", "distances", "food", "review", "tariff", "facilities", "faq"],
 "faq": [
   ("Do you have a hostel in Benachity or Sepco?",
    "No. All four Nottingville addresses are in City Center, Bidhannagar. We would rather tell you "
    "that upfront than have you travel to a viewing for a building that is not where you expected."),
   ("How far is City Center from the rest of Durgapur?",
    "City Center is centrally placed and well connected across Durgapur by bus, auto and toto. "
    "Call us and we will tell you the realistic travel time from your specific area."),
   ("Are all four buildings the same?",
    "They share the same food, the same rules and the same wardens. Room types and current "
    "availability differ, so ask us which building has what you need."),
 ],
 "wa": "Hi, I'd like to know which Nottingville location has availability.",
},
]


# ── Rendering ─────────────────────────────────────────────────────────────────
WA_SVG = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-'
          '.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-'
          '2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-'
          '.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-'
          '.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 '
          '2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118'
          '.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 '
          '7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 '
          '01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 '
          '012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 '
          '.16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 '
          '005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>')

PHONE_SVG = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
             '<path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.36 11.36 0 '
             '003.56.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.36 '
             '11.36 0 00.57 3.56 1 1 0 01-.25 1.02l-2.2 2.21z"/></svg>')


def wa_url(text, ref=""):
    """Prefilled WhatsApp message.

    `ref` appends the page slug so the owners see the source next to the
    sender's number in the WhatsApp inbox. Each LP maps 1:1 to an ad group,
    so the slug alone identifies the ad group. Deliberately not the gclid —
    a tracking string in a message a parent reads looks like spam.
    """
    if ref:
        text = f"{text}\n\nRef: {ref}"
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"


def block_food(p):
    cards = "".join(
        f'<div class="meal-card"><div class="meal-time">{t}</div>'
        f'<div class="meal-name">{n}</div><p class="meal-desc">{d}</p>'
        f'<span class="meal-tag">{tag}</span></div>'
        for t, n, d, tag in MEALS)
    return f'''
<section class="padded food-bg">
  <div class="container fade-in">
    <div class="eyebrow">The part families talk about</div>
    <h2 class="section-title">Four meals a day. <em>Six days non-veg.</em></h2>
    <p class="food-headline">&ldquo;Home like Food.&rdquo;</p>
    <p class="section-sub">The first line of our top Google review. It is the thing girls mention
      first and the thing parents check hardest, so we put it before everything else.</p>
    <div class="food-grid">{cards}</div>
    <div class="food-proof">
      <div><b>4</b><span>meals every single day, included in the rent</span></div>
      <div><b>6 days</b><span>non-vegetarian: chicken, fish and egg</span></div>
      <div><b>Rs 0</b><span>separate mess bill. It is all in the rent</span></div>
      <div><b>{RATING} &#9733;</b><span>from {REVIEW_COUNT} Google reviews</span></div>
    </div>
  </div>
</section>'''


def block_review(p):
    items = "".join(
        f'<div class="review-strip"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
        f'<p>&ldquo;{html.escape(q)}&rdquo; <span style="color:var(--muted)">&mdash; {src}</span></p></div>'
        for q, src in REVIEWS)
    return f'''
<section class="padded">
  <div class="container narrow fade-in">
    <div class="eyebrow">What families say</div>
    <h2 class="section-title">Rated <em>{RATING} out of 5</em> on Google</h2>
    <p class="section-sub">From {REVIEW_COUNT} reviews by the girls who live here and the parents who
      visit. Read them yourself before you decide.</p>
    {items}
  </div>
</section>'''


def block_pillars(p):
    return '''
<section class="padded" style="background:var(--parch)">
  <div class="container fade-in">
    <div class="eyebrow">Why parents choose us</div>
    <h2 class="section-title">Three things <em>that actually matter</em></h2>
    <div class="pillars-grid">
      <div class="pillar"><div class="pillar-icon">&#9679;</div>
        <h3>She eats properly</h3>
        <p>Four home-cooked meals a day, non-vegetarian six days a week, all included in the rent.
          Nobody has to survive on instant noodles before an exam.</p></div>
      <div class="pillar"><div class="pillar-icon">&#9679;</div>
        <h3>She is genuinely safe</h3>
        <p>24x7 CCTV, women wardens on site, gate closed at 7 PM, and a daily attendance register.
          Medical support arranged at any hour.</p></div>
      <div class="pillar"><div class="pillar-icon">&#9679;</div>
        <h3>Mothers run it</h3>
        <p>Three mothers, not a landlord and not a chain. They raise their own daughters in the same
          building, under the same rules.</p></div>
    </div>
  </div>
</section>'''


def block_facilities(p):
    items = "".join(
        f'<div class="fac-item"><span class="fac-icon">&#9670;</span>'
        f'<span class="fac-text"><b>{t}</b>{d}</span></div>' for t, d in FACILITIES)
    return f'''
<section class="padded">
  <div class="container fade-in">
    <div class="eyebrow">What is included</div>
    <h2 class="section-title">Everything she needs, <em>in the rent</em></h2>
    <div class="facilities-grid">{items}</div>
  </div>
</section>'''


def block_tariff(p):
    # data-l carries the column label so the row can restack as a labelled card
    # on narrow screens, where a 3-column grid wraps the rupee ranges badly.
    rate_rows = "".join(
        (f'<div class="tariff-row rate"><span class="room">{room}</span>'
         f'<b class="span2">{ac}</b></div>')
        if span else
        (f'<div class="tariff-row rate"><span class="room">{room}</span>'
         f'<b class="ac" data-l="AC">{ac}</b>'
         f'<b class="nonac" data-l="Non-AC">{nonac}</b></div>')
        for room, ac, nonac, span in TARIFF)
    return f'''
<section class="padded" style="background:var(--parch)">
  <div class="container narrow fade-in">
    <div class="eyebrow">What the fee covers</div>
    <h2 class="section-title">Room rates, <em>all meals included</em></h2>
    <p class="section-sub">Compare honestly: a cheaper bare room plus a mess subscription usually
      costs more than this, and the food is rarely home-cooked.</p>
    <div class="tariff">
      <div class="tariff-row rate head"><b>Room type</b><b>AC</b><b>Non-AC</b></div>
      {rate_rows}
    </div>
    <p class="tariff-note">Rates are per person, per month, and every one of them already includes
      all four meals, Aquaguard drinking water, free WiFi and 24x7 security. Non-AC rooms are
      Rs 500 to Rs 1,000 below the AC rate for the same occupancy. Four sharing starts at
      Rs 6,000, which is the lowest rate we offer.</p>
    <div class="tariff" style="margin-top:1.6rem">
      <div class="tariff-row head"><b>What every rate covers</b><b>Status</b></div>
      <div class="tariff-row"><span>Breakfast, lunch, evening snacks and tea, dinner</span><b class="inc">Included</b></div>
      <div class="tariff-row"><span>Non-vegetarian six days a week</span><b class="inc">Included</b></div>
      <div class="tariff-row"><span>Aquaguard drinking water</span><b class="inc">Included</b></div>
      <div class="tariff-row"><span>Free WiFi</span><b class="inc">Included</b></div>
      <div class="tariff-row"><span>24x7 CCTV, wardens, attendance register</span><b class="inc">Included</b></div>
      <div class="tariff-row"><span>Separate mess or tiffin charge</span><b class="inc">None</b></div>
    </div>
    <div style="margin-top:1.8rem;display:flex;gap:0.8rem;flex-wrap:wrap">
      <a href="tel:{TEL_PRIMARY}" class="btn-solid btn-primary-cta" data-cta="tariff-call">{PHONE_SVG} Ask for today&rsquo;s tariff</a>
      <a href="{wa_url(p['wa'], p['slug'])}" class="btn-wa" target="_blank" rel="noopener" data-cta="tariff-wa">Or WhatsApp</a>
    </div>
  </div>
</section>'''


def block_locations(p):
    cards = "".join(
        f'<div class="loc-card"><div class="loc-n">Location {i}</div>'
        f'<div class="loc-name">{n}</div><p>{a}</p></div>'
        for i, (n, a) in enumerate(LOCATIONS, 1))
    return f'''
<section class="padded" style="background:var(--parch)">
  <div class="container fade-in">
    <div class="eyebrow">Where we are</div>
    <h2 class="section-title">Four buildings, <em>all in City Center</em></h2>
    <p class="section-sub">Same food, same rules, same wardens across every address.</p>
    <div class="loc-grid">{cards}</div>
  </div>
</section>'''


def block_distances(p):
    # Deliberately no fabricated kilometre figures. These state the honest fact
    # (we are in City Center) and route the visitor to a phone call.
    areas = ["Benachity", "Sepco Township", "Muchipara", "Fuljhore",
             "Durgapur Station", "NSHM / coaching belt"]
    rows = "".join(
        f'<div class="distance-row"><b>{a}</b><span>Ask us the travel time</span></div>'
        for a in areas)
    return f'''
<section class="padded">
  <div class="container fade-in">
    <div class="eyebrow">Coming from elsewhere in Durgapur</div>
    <h2 class="section-title">We are in City Center. <em>Nowhere else.</em></h2>
    <p class="section-sub">We do not have a building in Benachity, Sepco, Muchipara or Fuljhore, and
      we will not claim otherwise. Call and we will give you the realistic travel time from your
      area before you make the trip.</p>
    <div class="distance-grid">{rows}</div>
    <div style="margin-top:1.8rem">
      <a href="tel:{TEL_PRIMARY}" class="btn-solid" data-cta="distance-call">{PHONE_SVG} Ask about your area</a>
    </div>
  </div>
</section>'''


def block_coaching(p):
    cards = "".join(f'<div class="institute-card"><div class="inst-name">{n}</div>'
                    f'<div class="inst-note">{note}</div></div>' for n, note in COACHING)
    pills = "".join(f'<span class="exam-pill">{e}</span>' for e in EXAMS)
    return f'''
<section class="padded" style="background:var(--parch)">
  <div class="container fade-in">
    <div class="eyebrow">For students</div>
    <h2 class="section-title">Near the <em>coaching belt</em></h2>
    <p class="section-sub">We are in City Center, Durgapur. Call us for the exact travel time to the
      centre she attends.</p>
    <div class="institute-grid">{cards}</div>
    <div class="exam-pill-group">{pills}</div>
  </div>
</section>'''


def block_faq(p):
    items = "".join(
        f'<div class="faq-item"><h3>{html.escape(q)}</h3><div class="faq-answer">{html.escape(a)}</div></div>'
        for q, a in p["faq"])
    return f'''
<section class="padded">
  <div class="container narrow fade-in">
    <div class="eyebrow">Questions families ask</div>
    <h2 class="section-title">Straight <em>answers</em></h2>
    <div class="faq-grid">{items}</div>
  </div>
</section>'''


BLOCKS = {"food": block_food, "review": block_review, "pillars": block_pillars,
          "facilities": block_facilities, "tariff": block_tariff,
          "locations": block_locations, "distances": block_distances,
          "coaching": block_coaching, "faq": block_faq}


def faq_schema(p):
    import json
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in p["faq"]]}, ensure_ascii=False, indent=1)


def lodging_schema(p):
    import json
    return json.dumps({
        "@context": "https://schema.org", "@type": "LodgingBusiness",
        "name": "Nottingville Hostel",
        "description": re.sub("<[^>]+>", "", p["desc"]),
        "url": f"{SITE}/{p['slug']}",
        "image": f"{SITE}/images/hostel-1.webp",
        "telephone": [t for t, _ in TEL_ALL],
        "priceRange": f"From INR {PRICE_FROM} to INR {PRICE_AC_SINGLE} per person per month",
        "address": [{"@type": "PostalAddress", "streetAddress": n,
                     "addressLocality": "Durgapur", "addressRegion": "West Bengal",
                     "postalCode": "713216", "addressCountry": "IN"}
                    for n, _ in LOCATIONS],
        "geo": {"@type": "GeoCoordinates", "latitude": 23.5204, "longitude": 87.3119},
        "numberOfRooms": 60,
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": x, "value": True}
            for x in ["4 meals daily included", "Non-vegetarian six days a week",
                      "AC & Non-AC Rooms", "Aquaguard drinking water", "Free WiFi",
                      "24x7 CCTV", "Women wardens", "Medical support"]],
    }, ensure_ascii=False, indent=1)
    # NOTE: aggregateRating is deliberately NOT marked up. The 4.6/17 reviews live
    # on Google, not on this site; self-marking third-party reviews breaches
    # Google's structured-data policy and risks a manual action. Displayed only.


def render(p):
    body = "".join(BLOCKS[b](p) for b in p["blocks"])
    points = "".join(f"<li>{x}</li>" for x in p["points"])
    footer_nav = "".join(
        f'<a href="/{s}">{l}</a>' for s, l in NAV_PAGES if s != p["slug"])
    phones = "".join(
        f'<a href="tel:{t}" class="phone-link" data-cta="footer-call">{d}</a>'
        for t, d in TEL_ALL)
    wa = wa_url(p["wa"], p["slug"])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}" />
<meta name="keywords" content="{p["keywords"]}" />
<link rel="canonical" href="{SITE}/{p["slug"]}" />
<meta property="og:title" content="{p["title"]}" />
<meta property="og:description" content="{p["desc"]}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{SITE}/{p["slug"]}" />
<meta property="og:image" content="{SITE}/images/hostel-1.webp" />
<meta property="og:site_name" content="Nottingville Hostel" />
<meta property="og:locale" content="en_IN" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#231008" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />

<!-- Google Ads tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-11090833551"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'AW-11090833551');
  function gads_phone_conversion() {{
    gtag('event', 'conversion', {{ 'send_to': 'AW-11090833551/3bdACMC1iIocEI_hwqgp' }});
  }}
  function gads_whatsapp_conversion() {{
    gtag('event', 'conversion', {{ 'send_to': 'AW-11090833551/RxJuCJffkoocEI_hwqgp' }});
  }}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet" />
<link rel="preload" as="image" href="/images/hostel-1.webp" />
<link rel="stylesheet" href="{CSS_URL}" />

<script type="application/ld+json">{lodging_schema(p)}</script>
<script type="application/ld+json">{faq_schema(p)}</script>
</head>
<body>

<nav id="nav">
  <a href="/" class="logo">Notting<span>ville</span></a>
  <div class="nav-right">
    <a href="tel:{TEL_PRIMARY}" class="nav-call" data-cta="nav-call">{PHONE_SVG} {TEL_ALL[0][1]}</a>
    <a href="{wa}" class="nav-wa" target="_blank" rel="noopener" data-cta="nav-wa">WhatsApp</a>
  </div>
</nav>

<header class="hero">
  <div class="hero-bg" id="heroBg"></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-badge">{p["badge"]}</div>
    <h1>{p["h1"]}</h1>
    <p class="hero-sub">{p["sub"]}</p>
    <div class="hero-price"><b>Rs {PRICE_FROM}</b><span>per month, four sharing &middot; all four meals included</span></div>
    <div class="hero-ctas">
      <a href="tel:{TEL_PRIMARY}" class="btn-white btn-primary-cta" data-cta="hero-call">{PHONE_SVG} Call {TEL_ALL[0][1]}</a>
      <a href="{wa}" class="btn-call" target="_blank" rel="noopener" data-cta="hero-wa">{WA_SVG} Or WhatsApp</a>
    </div>
  </div>
</header>

<div class="trust-bar">
  <div class="trust-item"><span class="trust-num">4</span><span class="trust-label">Meals Daily</span></div>
  <div class="trust-item"><span class="trust-num">6 Days</span><span class="trust-label">Non-Veg</span></div>
  <div class="trust-item"><span class="trust-num">{RATING}&#9733;</span><span class="trust-label">{REVIEW_COUNT} Google Reviews</span></div>
  <div class="trust-item"><span class="trust-num">24x7</span><span class="trust-label">CCTV &amp; Wardens</span></div>
</div>

<section class="padded answer-bg">
  <div class="container narrow fade-in">
    <p class="answer-lede">{p["lede"]}</p>
    <div class="ornament"><span class="orn-dot"></span><span class="orn-line"></span></div>
    <ul class="answer-points">{points}</ul>
  </div>
</section>
{body}
<section class="padded contact-bg" id="contact">
  <div class="container fade-in">
    <div class="eyebrow" style="color:rgba(255,255,255,0.75)">Admissions open 2026-27</div>
    <h2 class="section-title">Come and taste the food <em>before you decide</em></h2>
    <p class="contact-sub">Visit any of our four City Center addresses. Meet the wardens, see the
      rooms, and eat a meal with the girls. That is the honest way to choose.</p>
    <div class="contact-ctas">
      <a href="tel:{TEL_PRIMARY}" class="btn-white btn-primary-cta" data-cta="contact-call">{PHONE_SVG} Call {TEL_ALL[0][1]}</a>
      <a href="{wa}" class="btn-outline-white" target="_blank" rel="noopener" data-cta="contact-wa">{WA_SVG} Or WhatsApp</a>
    </div>
    <div class="phones">{phones}</div>
  </div>
</section>

<footer>
  <div class="footer-nav">{footer_nav}</div>
  <p><strong>Nottingville Hostel</strong> &nbsp;&middot;&nbsp; Girls&rsquo; Hostel &amp; PG, City Center, Durgapur
    &nbsp;&middot;&nbsp; <a href="{SITE}">nottingville.space</a></p>
  <p style="margin-top:0.5rem;">&copy; 2026 Nottingville. A hostel run by mothers, for daughters.</p>
</footer>

<a href="{wa}" class="wa-float" target="_blank" rel="noopener" aria-label="Chat on WhatsApp" data-cta="float-wa">{WA_SVG}</a>

<div class="sticky-cta">
  <a href="tel:{TEL_PRIMARY}" class="s-call" data-cta="sticky-call">{PHONE_SVG} Call now</a>
  <a href="{wa}" class="s-wa" target="_blank" rel="noopener" data-cta="sticky-wa">{WA_SVG} WhatsApp</a>
</div>

<script src="{JS_URL}" defer></script>
</body>
</html>
'''


def main():
    written = []
    for p in PAGES:
        out = ROOT / f"{p['slug']}.html"
        out.write_text(render(p), encoding="utf-8")
        written.append((p["slug"], out.stat().st_size))

    # sitemap: homepage + every landing page
    urls = "".join(
        f"\n  <url>\n    <loc>{SITE}/{s}</loc>\n    <lastmod>2026-07-22</lastmod>"
        f"\n    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>"
        for s, _ in written)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url>\n    <loc>{SITE}</loc>\n    <lastmod>2026-07-22</lastmod>\n'
        '    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>'
        f'{urls}\n</urlset>\n', encoding="utf-8")

    for s, n in written:
        print(f"  {s + '.html':<38} {n:>7,} B")
    print(f"\n  {len(written)} pages + sitemap.xml written")


if __name__ == "__main__":
    main()
