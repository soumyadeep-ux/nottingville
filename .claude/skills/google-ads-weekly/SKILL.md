---
name: google-ads-weekly
description: Weekly Google Ads check-in for Nottingville. Runs automated performance audit, flags waste, suggests optimizations.
user_invocable: true
---

# Google Ads Weekly Check-In — Nottingville

**Account ID:** 5886623748 | **Currency:** INR | **Goal:** More relevant calls/WhatsApp leads

Run this check-in every week. Execute ALL steps in order.

## Step 1: Performance Summary (Last 7 Days vs Previous 7)

Run these two GAQL queries via `mcp__google-ads__run_gaql`:

**Last 7 days:**
```sql
SELECT campaign.name, campaign.status, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions, metrics.ctr, metrics.average_cpc
FROM campaign
WHERE campaign.status != 'REMOVED'
AND segments.date DURING LAST_7_DAYS
ORDER BY metrics.cost_micros DESC
```

**Previous 7 days** (calculate dates: 14 days ago to 8 days ago):
```sql
SELECT campaign.name, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions
FROM campaign
WHERE campaign.status != 'REMOVED'
AND segments.date BETWEEN '{14_days_ago}' AND '{8_days_ago}'
ORDER BY metrics.cost_micros DESC
```

**Present as a comparison table:**
| Metric | This Week | Last Week | Change |
|---|---|---|---|
| Clicks | | | |
| Impressions | | | |
| Spend (INR) | | | |
| Conversions | | | |
| CPA (INR) | | | |
| CTR | | | |
| Avg CPC | | | |

Flag: CPA spike >20%, CTR drop >15%, budget capped (spend >= 95% of daily budget × 7).

## Step 2: Search Terms Audit

```sql
SELECT search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_7_DAYS
ORDER BY metrics.clicks DESC
LIMIT 30
```

**Classify each search term:**
- **Converting** — keep, consider adding as keyword
- **Relevant but not converting yet** — watch (need more data)
- **Irrelevant / waste** — add as negative keyword immediately
- **Job seeker / informational** — add as negative keyword

**Red flags to auto-detect:**
- Any "near me" without Durgapur context
- Boys hostel / male related queries
- Other city names (Kolkata, Delhi, etc.)
- Job/career/salary related
- Hotel/resort/OYO related
- Allen/Aakash fees (wanting the coaching institute's own hostel)

**Action:** Add waste terms as negative keywords using `mcp__google-ads__add_negative_keywords`.

## Step 3: Keyword Performance

```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group.name, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions, metrics.average_cpc
FROM keyword_view
WHERE segments.date DURING LAST_7_DAYS
AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
LIMIT 20
```

**Flag:**
- Keywords with 50+ clicks and 0 conversions → consider pausing
- Keywords with CVR > 5% → consider raising bid
- Keywords with < 3 impressions/day → check match type, may need broadening

## Step 4: Quality Score Check

```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.search_predicted_ctr, ad_group_criterion.quality_info.post_click_quality_score, metrics.impressions
FROM keyword_view
WHERE ad_group_criterion.status = 'ENABLED'
AND metrics.impressions > 10
ORDER BY ad_group_criterion.quality_info.quality_score ASC
LIMIT 20
```

**Flag:** Any keyword with QS < 5 that has significant impressions. Note which component is "BELOW_AVERAGE".

## Step 5: Ad Group Performance

```sql
SELECT ad_group.name, ad_group.status, campaign.name, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions, metrics.ctr
FROM ad_group
WHERE campaign.status = 'ENABLED'
AND segments.date DURING LAST_7_DAYS
ORDER BY metrics.cost_micros DESC
```

Compare performance across ad groups. Check if one ad group is consuming disproportionate budget.

## Step 6: Budget Check

```sql
SELECT campaign.name, campaign_budget.amount_micros, metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
AND segments.date DURING LAST_7_DAYS
```

Calculate: `actual_daily_spend = cost_micros / 7 / 1_000_000`
Compare to: `daily_budget = budget_amount_micros / 1_000_000`

If spend >= 95% of budget → campaign is budget-capped → consider increasing budget or tightening targeting.

## Step 7: Conversion Tracking Verification

Run Playwright check (optional, do monthly):
```bash
node /tmp/check-gtag.mjs
```

Verify:
- gtag.js loads on nottingville.space
- AW-11090833551 tag present
- gads_whatsapp_conversion() and gads_phone_conversion() functions exist
- Network requests to Google fire on page load

## Step 8: Weekly Report

**Summarize findings as:**

### This Week's Performance
[comparison table from Step 1]

### Search Term Issues
- [X waste terms found, added as negatives]
- [any new keyword opportunities]

### Anomalies
- [list any flags from steps above]

### Actions Taken
- [negatives added]
- [keywords paused/added]
- [bids changed]
- [budget changes]

### Next Week's Focus
- [what to watch]

---

## Reference
- **Strategy doc:** `google-ads-strategy.md` in project root
- **Account ID:** 5886623748
- **Conversion labels:** WhatsApp = `RxJuCJffkoocEI_hwqgp`, Phone = `3bdACMC1iIocEI_hwqgp`
- **Historical CPA:** INR 458 (old campaign), target: INR 200-400 (new)
- **Historical CVR:** 2.73% (old), target: 3-5% (new, tighter targeting)
