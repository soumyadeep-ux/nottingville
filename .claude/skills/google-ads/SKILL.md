---
name: google-ads
description: >
  Use when the user asks about Google Ads campaign performance, ad spend, ROAS, CPA,
  keywords, search terms, quality scores, impression share, budget projections,
  account audits, or wants to pause campaigns, change bids, update budgets, add keywords,
  or create ads. Also use for PPC math and forecasting calculations.
---

# Google Ads

Senior Google Ads analyst with live MCP access to 48+ accounts under Ekamoira Marketing MCC.

## MCP Tools

| Tool | Purpose |
|---|---|
| `list_accounts` | List all accounts under MCC |
| `execute_gaql_query` | Run custom GAQL queries |
| `get_campaign_performance` | Campaign metrics with date range |
| `get_ad_performance` | Ad creative performance |
| `run_gaql` | Arbitrary GAQL (table/JSON/CSV format) |
| `get_image_assets` | List image assets |
| `get_ad_creatives` | Ad creative details |
| `get_asset_usage` | Where assets are used |
| `analyze_image_assets` | Image asset performance |
| `get_account_currency` | Account currency |

**Always pass the client's customer ID** (not MCC ID `8952449784`) as the account parameter.

## GAQL Quick Start

See `gaql-reference.md` for complete query templates (campaigns, search terms, keywords, devices, geo, ads, extensions, conversions, impression share, hourly/daily performance).

```sql
SELECT field1, field2 FROM resource WHERE condition ORDER BY field LIMIT n
```

- **Attributes**: `campaign.name`, `campaign.status`
- **Metrics**: `metrics.clicks`, `metrics.cost_micros`
- **Segments**: `segments.date`, `segments.device` (splits results — use sparingly)
- **Cost**: API returns micros. `cost_micros / 1,000,000` = currency unit. Always show 2 decimal places.
- **Dates**: `DURING LAST_30_DAYS`, `BETWEEN '2026-01-01' AND '2026-01-31'`
- **Filter dead entities**: `AND campaign.status != 'REMOVED'`

---

## Strategy Determination Framework

Before making recommendations, classify the account situation to determine the right strategic approach.

### Step 1: Assess Account Maturity

| Signal | New/Broken Account | Established Account |
|---|---|---|
| Conversions/month | <10 | 30+ |
| Negative keywords | <50 | 200-500+ |
| Quality Scores | Mostly 3-5 | Mostly 6-8 |
| Search term relevance | <50% on-intent | >80% on-intent |
| Bidding strategy | Should be Manual CPC | Can use tCPA/tROAS |

### Step 2: Determine Budget Viability Per Geo

For each target geography, calculate whether paid ads are viable:

```
Viable = (Monthly Search Volume for keyword cluster) >= 250
  AND (Monthly Budget / Avg CPC) >= 100 clicks
  AND (Expected Clicks / CVR) >= target leads
```

**Minimum viable daily budgets by market:**

| Market Type | Min Daily Budget | Typical CPC Range | Clicks/Day at Min Budget |
|---|---|---|---|
| India (IT services) | INR 1,000-2,000 | INR 50-300 | 5-40 |
| UAE/Gulf | INR 2,500-4,000 | INR 500-3,500 | 1-8 |
| APAC (AU/SG) | INR 1,500-3,000 | INR 200-1,500 | 2-15 |
| US/UK | INR 3,000-5,000 | INR 400-2,500 | 2-12 |

### Step 3: Budget Allocation Across Geos

**Golden rule:** Always use separate campaigns per country. Never pool budgets across geos — the highest-volume market will eat everything.

**Allocation framework (for a fixed total budget):**

1. **Calculate lead cost per geo:** `Target CPA = Monthly Budget for Geo / Target Leads`
2. **Check feasibility:** Is the target CPA achievable given market CPCs and CVR?
3. **Prioritize by ROI:** Allocate more to geos where CPA is lowest relative to lead value
4. **Set floors:** Each geo needs minimum viable budget (see table above) or don't run it

**Example: INR 100,000 total budget, 6-8 leads/geo target:**

| Geo | Allocation | Daily Budget | Target CPA | Feasibility Check |
|---|---|---|---|---|
| India | INR 30,000 (30%) | INR 1,000/day | INR 3,750-5,000 | Achievable if QS >= 5 and CPCs ~INR 100-200 |
| Gulf/UAE | INR 45,000 (45%) | INR 1,500/day | INR 5,625-7,500 | Tight — UAE CPCs are INR 500-3,500/click |
| APAC | INR 25,000 (25%) | INR 833/day | INR 3,125-4,167 | Risky — low search volume, test for 30 days |

**Decision tree for underfunded geos:**
- If budget < 10 clicks/day for a geo → don't run paid ads, use SEO/content instead
- If target CPA < 3x average CPC → mathematically impossible, reallocate budget
- If search volume < 250/month for keyword cluster → not enough demand for paid

### Step 4: Identify Structural Problems First

Before optimizing bids or copy, check these account-health fundamentals:

1. **Wasted spend %** — What % of budget goes to irrelevant search terms? (>30% = critical)
2. **Conversion tracking accuracy** — Duplicates? MANY_PER_CLICK counting? Gmail signups inflating?
3. **Negative keyword coverage** — <50 negatives in a B2B IT services account = guaranteed waste
4. **Quality Score distribution** — All QS 3/10? Fix landing pages before touching bids
5. **Job seeker contamination** — IT services keywords attract massive job-seeker traffic (see below)

---

## Search Term Intent Classification

Every search term analysis must classify terms by intent. This determines bid strategy, negative keywords, and campaign structure.

### The Four-Intent Framework

| Intent | Signal Words | CVR Range | Action |
|---|---|---|---|
| **Transactional** | hire, services, company, agency, provider, near me, pricing, quote, outsource | 5-15% | Highest bids, dedicated campaigns |
| **Commercial** | best, top, compare, vs, review, alternative, recommended | 3-8% | Medium-high bids, comparison LPs |
| **Informational** | how to, what is, guide, tutorial, why, tips, definition, meaning | <1% | EXCLUDE from paid or remarket only |
| **Navigational** | [brand name], [competitor name], login, website, official | Variable | Brand: defend. Competitor: test or negate |

### IT Services Intent Patterns

**Transactional (BID HIGH):**
```
"QA testing company" / "hire QA testers" / "VAPT services provider"
"mobile app development agency" / "outsource software testing"
"penetration testing company near me" / "QA consulting services"
"software testing company in [city]" / "app developers near me"
```

**Commercial (BID MEDIUM):**
```
"best QA testing companies" / "top app development agencies India"
"VAPT vs penetration testing" / "manual vs automated testing services"
```

**Informational (EXCLUDE):**
```
"what is QA testing" / "how to do penetration testing"
"VAPT meaning" / "software testing types" / "QA testing tutorial"
```

**Job Seeker (ALWAYS EXCLUDE):**
```
"QA testing jobs" / "software tester salary" / "QA engineer resume"
"app developer hiring" / "testing company careers"
```

### Weekly Classification Workflow

1. Pull Search Terms Report (last 7 days)
2. Classify each query into intent bucket
3. Transactional: keep, raise bids if converting
4. Commercial: keep, test ad copy and LPs
5. Informational: add as negative (phrase match)
6. Job-seeker: add as negative immediately
7. Track ratio — aim for >70% transactional queries

**Impact:** Intent-aligned campaigns achieve up to 220% higher CTR vs keyword-only approaches.

---

## Job Search Query Filtering (B2B IT Services)

IT service keywords (QA testing, app development, VAPT, software testing) attract massive job-seeker traffic. This is the #1 source of wasted spend for B2B IT services accounts.

### Pre-Launch Negative Keyword Lists

Apply ALL of these as **account-level** negatives (phrase match) before any campaign goes live:

**Core Job Terms:**
```
job, jobs, career, careers, employment, hiring, recruit, recruiting, recruitment,
vacancy, vacancies, opening, openings, position, positions, freelance,
contractor, employee, staff, staffing
```

**Compensation Terms:**
```
salary, salaries, pay, wages, compensation, benefits, package, CTC, stipend,
hourly rate, annual salary, pay scale
```

**Application Terms:**
```
resume, CV, cover letter, application, apply, applying, interview, interviewing,
portfolio, reference, background check
```

**Experience Level Terms:**
```
intern, internship, fresher, freshers, entry level, junior, trainee, apprentice,
graduate
```

**Education/Certification Terms:**
```
course, courses, certification, certified, training, learn, learning, tutorial,
syllabus, exam, ISTQB, study, bootcamp, degree, diploma, what is, definition,
meaning, for beginners
```

**India-Specific Job Terms (critical for India campaigns):**
```
Naukri, placement, campus, walkin, walk-in, off campus, on campus,
TCS, Infosys, Wipro, Cognizant, Accenture
```

**Platform/Job Board Terms:**
```
Glassdoor, Indeed, LinkedIn jobs, Monster
```

### Implementation Rules

- **Match type:** Phrase match for job negatives (catches variations)
- **Level:** Account-level for universal exclusions (limit: 1,000 keywords)
- **Review cadence:** Weekly for first 30 days, then biweekly
- **Target:** High-performing B2B accounts maintain 200-500+ negative keywords
- **Impact:** Proactive negatives typically reduce irrelevant clicks by 40%+

---

## Negative Keyword Strategy (Complete)

### Account-Level vs Campaign-Level

| Level | Limit | Use For |
|---|---|---|
| Account-level | 1,000 keywords | Universal: jobs, free, DIY, educational, competitors |
| Campaign-level lists | 5,000 per list, 20 lists max | Campaign-specific exclusions |
| Performance Max | 10,000 per campaign | PMax-specific negatives |
| Ad group-level | Unlimited (practical ~1,000) | Traffic shaping between ad groups |

### Complete Categories for B2B IT Services

**1. Job Seekers** (see section above — HIGHEST PRIORITY)

**2. DIY/How-To/Free:**
```
DIY, do it yourself, how to, self, build your own, free, cheap, discount,
budget, affordable, low cost, open source, template, sample, trial, freemium
```

**3. No-Code/Low-Code Platforms (for app dev campaigns):**
```
kodular, thunkable, bubble, glide, appsgeyser, mit app inventor, no-code,
low code, app maker, app creator, apk maker, app builder ai, how to make,
how to create, how to build, kaise banaye
```

**4. Competitor Tools (context-dependent — only negate if NOT running competitor campaigns):**
```
[Add competitor tool names: pentestgpt, browserstack, postman, etc.]
[Add competitor company names: testcrew, virtuoso qa, etc.]
```

**5. Generic Testing Tools (for QA/testing campaigns):**
```
playwright, k6, firebase, ghost inspector, selenium tutorial, jmeter download,
rest assured, karate automation, cypress tutorial
```

**6. Consumer/B2C Terms:**
```
home, personal, individual, single, residential, consumer, household, hobbyist
```

---

## Bidding Strategy Selection

### Decision Matrix

| Scenario | Strategy | Why |
|---|---|---|
| New account, no conversion data | **Manual CPC** | Full control while learning |
| Gathering data, <15 conv/mo | **Maximize Clicks** (with max CPC cap) | Build click data without overspending |
| 15-30 conversions/month | **Maximize Conversions** (no target) | Enough data for basic automation |
| 30+ conv/month, stable CPA | **Target CPA** | Stabilize and scale with CPA ceiling |
| Variable lead values, 30+ conv/mo | **Target ROAS** | Optimize for value, not volume |
| Brand campaigns | **Target Impression Share** | Secure top placements |

### Conversion Threshold Requirements

| Strategy | Minimum Conv (30-day) | Google's Recommendation |
|---|---|---|
| Manual CPC | 0 | N/A |
| Maximize Clicks | 0 | N/A |
| Maximize Conversions | ~5 | More is better |
| Target CPA | **15 minimum** | **30-50 per campaign** |
| Target ROAS | **15 minimum** | **50+ per campaign** |

**Critical rule:** Daily budget must be **2-3x your target CPA** for tCPA to function. If target CPA = INR 5,000, daily budget needs INR 10,000-15,000 minimum.

### eCPC Deprecation (March 2025)

Enhanced CPC was deprecated for Search and Display. Campaigns not migrated were auto-switched to Manual CPC. Do not recommend eCPC.

### Progressive Strategy Path

```
Week 1-4:   Manual CPC or Maximize Clicks (gather data, learn CPCs)
                    ↓ (once 15+ conversions/month)
Month 2-3:  Maximize Conversions (let Google optimize freely)
                    ↓ (once 30+ conversions/month with stable CPA)
Month 3+:   Target CPA (set ceiling, scale)
```

### For Accounts with <10 Conversions/Month (Common in B2B)

1. **Stick with Manual CPC** — maintain control
2. **Maximize Clicks + max CPC cap** — prevents overspend while building data
3. **Broaden conversion definition** — count micro-conversions (PDF downloads, 60s+ visits) as secondary conversions to feed the algorithm
4. **Never use tCPA with <15 conversions** — the algorithm will swing wildly

---

## Device-Level Analysis

### B2B Device Performance Pattern

| Device | Research Usage | Conversion Rate | Typical B2B Action |
|---|---|---|---|
| Desktop | 40% of research | **Highest** | Form fills, demo requests, long-form reading |
| Mobile | 60% of initial research | **Lower** | Quick searches, calls, bookmarking |
| Tablet | <5% | **Lowest** | Light browsing, rarely converts for B2B |

### Starting Bid Adjustments

| Device | Adjustment | Rationale |
|---|---|---|
| Desktop | +0% to +20% | Primary B2B conversion device |
| Mobile | -20% to -30% | Lower CVR, but don't exclude entirely |
| Tablet | -50% | Very low B2B conversion rate |

### When to Use Separate Campaigns vs Bid Adjustments

**Bid adjustments when:** Single LP experience, limited budget, moderate performance gap (20-30%)
**Separate campaigns when:** Distinct mobile/desktop LPs, dramatic performance difference (3x+), need separate budgets

### Data Requirements Before Adjusting

- Wait for **100+ clicks per device** before making adjustments
- Review over **2-4 week windows**, not days
- Key metric: cost per conversion and CVR, not just CTR
- Always query device data when auditing (see GAQL reference)

### Layered Targeting (Advanced)

Combine device bids with time-of-day for maximum precision:
- Desktop + Business Hours (9 AM-5 PM weekdays): +20%
- Mobile + Lunch Hours (11 AM-2 PM weekdays): +10%
- Mobile + Weekends: -40%
- Tablet + Any time: -50%

---

## Spending Pattern Analysis

### B2B Time-of-Day Performance Data

| Time Window | % of Leads | CPL vs Average | Recommended Action |
|---|---|---|---|
| 8 AM-12 PM (weekdays) | 48.7% | -38% (cheapest) | **Max bid** |
| 1 PM-4 PM (weekdays) | 39.7% | -37% | **Max bid** |
| Mon-Wed, 10 AM-3 PM | Peak | +30% conv rate | **Golden window** — increase bids |
| 4 PM-8 PM | Low | Above avg CPL | Reduce bids -20% |
| 8 PM-12 AM | Very low | Wasted | **Exclude or -90%** |
| 12 AM-5 AM | Zero | 100% waste | **Exclude** |
| Weekends | 25.6% | +51% higher CPL | Reduce -30% or exclude |

**Key stats:**
- 10.8% of budget typically wasted on zero-conversion hours (late night/evening)
- Weekend CPL is 51% higher than weekdays
- Mon-Thu generates 74.4% of all B2B leads
- 8 AM-4 PM drives 88.4% of leads while consuming only 72.5% of budget

### Recommended Ad Schedule (B2B IT Services)

```
Monday-Wednesday:  6 AM - 8 PM  (+20% bid during 10 AM-3 PM)
Thursday:          6 AM - 8 PM  (+0%)
Friday:            6 AM - 6 PM  (-10%)
Saturday:          9 AM - 2 PM  (-30%) or OFF
Sunday:            OFF
```

**India campaigns:** Adjust to IST (9:30 AM - 6:30 PM business hours)
**Gulf campaigns:** Adjust to GST (Sun-Thu work week, Fri-Sat weekend)

### Optimization Impact

By implementing ad scheduling:
- +18-25% more leads per week
- 14-18% lower CPL
- No increase in total budget required

### Budget Pacing Warning (2025+)

Google now paces budgets to spend up to 30.4x daily budget monthly — even with ad scheduling. A INR 1,000/day budget with Mon-Fri scheduling could spend INR 30,400/month (not INR 22,000). Monitor actual spend.

---

## Volume Limitations & Low-Volume Markets

### Viability Assessment

| Monthly Searches (cluster) | Viability | Action |
|---|---|---|
| <10 per keyword | Not viable | Google marks "Low search volume", won't show ads |
| 10-100 | Marginal | Combine into broader match groups |
| 100-500 | Low but testable | Maximize Clicks, expect slow data |
| 500-3,000 | Viable for niche B2B | Standard campaign, realistic expectations |
| 3,000+ | Strong | Full campaign structure |

### When Paid Ads Are NOT Viable

- Total search volume <100/month AND CPC >$5
- Niche dominated by job seekers/students
- Service so new nobody searches for it (use demand gen)
- Math doesn't work: if CPL > 20% of deal value

### Cost Per Test Click Methodology

To evaluate a new market before committing:
1. Average B2B CVR: 5.14% → need ~20 clicks for 1 conversion
2. For statistical confidence (10 conversions): ~200 clicks
3. If CPC = INR 200 (India): test cost = INR 40,000
4. If CPC = INR 2,500 (UAE): test cost = INR 500,000
5. Minimum test period: 30 days
6. Decision: Got conversions? Scale. Got 200+ clicks, zero conversions? LP or targeting issue. Barely any impressions? Market too small.

### Alternatives for Low-Volume Markets

1. Broader match types (phrase/broad instead of exact)
2. Remarketing as primary channel
3. Content/SEO + retargeting hybrid
4. Dynamic Search Ads (let Google match LPs to queries)

---

## Quality Score Reference

### QS CPC Modifier Table

QS 5 is baseline (no discount/penalty):

| QS | CPC Modifier | Example (base INR 300) |
|---|---|---|
| **10** | -50% discount | INR 150 |
| **9** | -44% discount | INR 168 |
| **8** | -37% discount | INR 189 |
| **7** | -29% discount | INR 213 |
| **6** | -17% discount | INR 249 |
| **5** | 0% baseline | INR 300 |
| **4** | +25% penalty | INR 375 |
| **3** | +67% penalty | INR 501 |
| **2** | +150% penalty | INR 750 |
| **1** | +400% penalty | INR 1,500 |

**The math:** QS 3 → QS 7 on INR 300 CPC saves INR 288/click. Over 500 clicks/month = INR 144,000/month saved.

### Three Components

| Component | Weight | Fix |
|---|---|---|
| Expected CTR | ~39% | Keyword in Headline 1, specific CTA, numbers, extensions |
| Landing Page Experience | ~39% | Sub-2s load, mobile-responsive, keyword in H1, trust signals |
| Ad Relevance | ~22% | Mirror keyword language, tight ad groups, DKI |

### "3 to 6" Playbook

1. Check which components are "Below Average"
2. Expected CTR below avg → rewrite ads, add keyword to headline, add extensions
3. Ad Relevance below avg → tighten ad groups (split), use DKI
4. Landing Page below avg → improve speed, add keyword content, fix mobile
5. Recheck in 2-4 weeks (QS updates lag)

---

## Anomaly Detection (Auto-Flag)

Flag these automatically in any analysis output:

| Anomaly | Threshold | Severity |
|---|---|---|
| Zero-conversion spend | Spend > INR 5,000 and 0 conversions | Critical |
| Job-seeker query contamination | >10% of clicks from job/salary/career terms | Critical |
| CPA spike | CPA increased > 20% vs previous period | High |
| Budget capped | Spend >= 95% of daily budget | High |
| Low Quality Score | QS < 5 on keywords with > 100 impressions | Medium |
| CTR drop | CTR decreased > 15% vs previous period | Medium |
| IS loss (budget) | > 20% lost to budget | High |
| IS loss (rank) | > 30% lost to rank | Medium |
| After-hours spend | >5% of budget between 9 PM-6 AM | Medium |
| Weekend waste | Weekend CPL > 40% higher than weekday | Medium |
| No negative keywords | Account has <50 negatives for B2B IT services | Critical |
| tCPA with <15 conv | Target CPA bidding with insufficient data | High |

---

## PPC Math

| Metric | Formula |
|---|---|
| CPA | Spend / Conversions |
| ROAS | Revenue / Spend |
| CTR | Clicks / Impressions |
| CPC | Spend / Clicks |
| CVR | Conversions / Clicks |
| Break-Even ROAS | 1 / Profit Margin |
| Monthly Spend | Daily Budget * 30.4 |
| IS Opportunity | Missed Impr = Total Impr * ((1 - IS) / IS) |
| Leads from Budget | (Monthly Budget / Avg CPC) * CVR |
| Required Budget for N Leads | (N / CVR) * Avg CPC |
| Max Viable CPC | (Target CPA * CVR) |

Always show inputs, formula, result. Offer sensitivity analysis.

### B2B Benchmarks (2025)

| Metric | Business Services Avg |
|---|---|
| Avg CPC (global) | $5.58 |
| Avg CPL | $103.54 |
| Avg CVR (Search) | 5.14% |
| Avg CTR | 5.65% |
| CPC YoY inflation | 12.88% |
| First-visit conversion | 2% (98% need retargeting) |

---

## Account Audit (7 Dimensions)

When asked to audit, check all 7 systematically. **Always use LAST_90_DAYS for audits** (30 days is too short for B2B with low conversion volume):

1. **Structure** — naming, ad group themes, campaign types, budget alignment, paused campaign bloat
2. **Conversions** — tracking setup, attribution model, counting (ONE vs MANY), value tracking, duplicates
3. **Keywords** — match types, QS distribution, negative coverage, search term relevance, job-seeker contamination
4. **Creative** — RSA ad strength, headline/description count, extensions, landing page relevance
5. **Bidding & Budget** — strategy per campaign vs conversion volume, budget utilization, capped campaigns, device adjustments
6. **Targeting** — geo performance, device variance, ad schedule, audiences, time-of-day waste
7. **Wasted Spend** — irrelevant search terms, zero-conv keywords, low-QS spend, underperforming geos, job-seeker waste, after-hours spend

**Output format:** Score X/10 per dimension, then Critical/High/Medium/Low issues with Impact and Fix. End with:
- Estimated total wasted spend (monthly)
- Wasted spend by category (job seekers, competitors, DIY, informational, after-hours)
- Top 3 quick wins
- Budget reallocation recommendation
- 30/60/90-day action plan

---

## Write Operations — CEP Protocol

**Every mutation requires Confirm -> Execute -> Post-check. No exceptions.**

### Step 1: Confirm

Before ANY write, first query current state, then present:

```
## Proposed Change
**Action**: [what will happen]
**Account**: [customer ID and name]
**Target**: [entity name and ID]
**Before**: [current state from query]
**After**: [new state]
**Risk Level**: [Low/Medium/High]

Type CONFIRM to proceed.
```

### Step 2: Execute
Only after user explicitly says "confirm", "yes", "go ahead", or "do it".

### Step 3: Post-check
Re-query the entity. Report before/after comparison.

### Safety Rules

1. **One confirmation per mutation** — if user asks to pause a campaign AND change its budget, present TWO separate confirmations
2. **Never skip confirmation** — even if user says "just do it all"
3. **Always query before-state first**
4. **Create campaigns and ads PAUSED** — never ENABLED by default
5. **Flag shared budgets** — warn about linked campaigns
6. **Batch limit** — max 50 keyword additions per batch, with itemized preview
7. **Note rollback** — after every write, state how to reverse it

### Common Operations

| Operation | Risk | Key Check |
|---|---|---|
| Pause/enable campaign | Medium | Affects all ads in campaign |
| Update budget | Medium | Shared budget? Monthly = daily * 30.4 |
| Update keyword bid | Low | Show current vs new bid |
| Add negative keywords | Low | Show match types, affected campaigns |
| Create RSA ad | Low | Create PAUSED, validate char limits (30/90) |
| Create campaign | High | Create PAUSED, confirm budget and targeting |

---

## Multi-Account Workflow

**Key accounts** (run `list_accounts` for full current list):

| Account | ID |
|---|---|
| Ekamoira Marketing MCC | 8952449784 |
| Ekamoira Europe | 3051641631 |
| Ekamoira India | 1151572298 |
| Vervali Systems India | 9355469827 |

For cross-account analysis: query each account separately, normalize metrics, note currency differences.

---

## Rate Limits

Basic Access: 15,000 ops/day. Use `LIMIT`, filter `status != 'REMOVED'`, avoid unnecessary segments.
