# GAQL Query Reference

## Syntax

```sql
SELECT field1, field2, ...
FROM resource
WHERE condition
ORDER BY field [ASC|DESC]
LIMIT n
```

Three field categories:
- **Attributes**: Resource properties (`campaign.name`, `campaign.status`)
- **Metrics**: Performance data (`metrics.clicks`, `metrics.cost_micros`)
- **Segments**: Grouping dimensions (`segments.date`, `segments.device`) — splits results, use sparingly

## Date Ranges

```sql
WHERE segments.date DURING LAST_7_DAYS
WHERE segments.date DURING LAST_30_DAYS
WHERE segments.date DURING LAST_90_DAYS
WHERE segments.date DURING THIS_MONTH
WHERE segments.date DURING LAST_MONTH
WHERE segments.date DURING THIS_QUARTER
WHERE segments.date BETWEEN '2026-01-01' AND '2026-01-31'
```

**Tip**: Adding `segments.date` splits metrics by day. Only add if you need daily breakdown.
**For audits**: Use LAST_90_DAYS for B2B accounts (30 days has too few conversions for reliable analysis).

## Campaign Performance

```sql
SELECT
  campaign.id, campaign.name, campaign.status,
  campaign.advertising_channel_type, campaign.bidding_strategy_type,
  campaign_budget.amount_micros,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.conversions_value,
  metrics.ctr, metrics.average_cpc, metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

## Campaign with Bidding Strategy Details

```sql
SELECT
  campaign.id, campaign.name, campaign.status,
  campaign.bidding_strategy_type,
  campaign.target_cpa.target_cpa_micros,
  campaign.maximize_conversions.target_cpa_micros,
  campaign.maximize_conversion_value.target_roas,
  campaign_budget.amount_micros,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.cost_per_conversion
FROM campaign
WHERE campaign.status != 'REMOVED'
  AND segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Search Terms (Wasted Spend)

```sql
SELECT
  search_term_view.search_term, search_term_view.status,
  campaign.name, ad_group.name,
  metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.conversions = 0
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

## Search Terms (All — for intent classification)

```sql
SELECT
  search_term_view.search_term,
  campaign.name, ad_group.name,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.ctr
FROM search_term_view
WHERE segments.date DURING LAST_90_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

## Search Terms (Job Seeker Detection)

Look for job/salary/career terms in search term report. Query all terms then filter client-side for:
`job`, `jobs`, `career`, `salary`, `hiring`, `fresher`, `resume`, `intern`, `vacancy`, `naukri`, `placement`

```sql
SELECT
  search_term_view.search_term,
  metrics.cost_micros, metrics.clicks, metrics.impressions
FROM search_term_view
WHERE segments.date DURING LAST_90_DAYS
  AND metrics.clicks > 0
ORDER BY metrics.cost_micros DESC
LIMIT 500
```

## Keyword Quality Scores

```sql
SELECT
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  campaign.name, ad_group.name,
  metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Device Performance (Account-Level)

```sql
SELECT
  segments.device,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.conversions_value,
  metrics.ctr, metrics.average_cpc, metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
```

## Device Performance (Per Campaign)

```sql
SELECT
  campaign.name, segments.device,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.ctr, metrics.average_cpc,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY campaign.name, metrics.cost_micros DESC
```

## Device Bid Adjustments (Current Settings)

```sql
SELECT
  campaign.name,
  campaign_criterion.device.type,
  campaign_criterion.bid_modifier
FROM campaign_criterion
WHERE campaign_criterion.type = 'DEVICE'
  AND campaign.status != 'REMOVED'
```

## Hour-of-Day Performance

Use `segments.hour` (0-23) to identify time-of-day patterns. Essential for B2B ad schedule optimization.

```sql
SELECT
  segments.hour,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.ctr, metrics.average_cpc
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY segments.hour
```

## Hour-of-Day Performance (Per Campaign)

```sql
SELECT
  campaign.name, segments.hour,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY campaign.name, segments.hour
```

## Day-of-Week Performance

Use `segments.day_of_week` (MONDAY, TUESDAY, ..., SUNDAY) for day patterns.

```sql
SELECT
  segments.day_of_week,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.ctr, metrics.average_cpc,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

## Day-of-Week Performance (Per Campaign)

```sql
SELECT
  campaign.name, segments.day_of_week,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY campaign.name
```

## Ad Schedule Settings (Current)

```sql
SELECT
  campaign.name,
  campaign_criterion.ad_schedule.day_of_week,
  campaign_criterion.ad_schedule.start_hour,
  campaign_criterion.ad_schedule.end_hour,
  campaign_criterion.bid_modifier
FROM campaign_criterion
WHERE campaign_criterion.type = 'AD_SCHEDULE'
  AND campaign.status != 'REMOVED'
```

## Impression Share

```sql
SELECT
  campaign.name,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.advertising_channel_type = 'SEARCH'
```

## Geographic Performance

```sql
SELECT
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions, metrics.conversions_value
FROM geographic_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

## Geographic Performance (By Campaign)

```sql
SELECT
  campaign.name,
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  metrics.cost_micros, metrics.clicks, metrics.impressions,
  metrics.conversions
FROM geographic_view
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
LIMIT 100
```

## Ad Creative Performance (RSA)

```sql
SELECT
  ad_group_ad.ad.id,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  ad_group_ad.ad.final_urls,
  ad_group_ad.ad_strength,
  campaign.name, ad_group.name,
  metrics.clicks, metrics.impressions, metrics.ctr,
  metrics.conversions, metrics.cost_micros
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_ad.status != 'REMOVED'
ORDER BY metrics.impressions DESC
```

## Ad Extensions / Assets

```sql
SELECT
  asset.name, asset.type,
  campaign.name,
  metrics.clicks, metrics.impressions
FROM campaign_asset
WHERE segments.date DURING LAST_30_DAYS
```

## Conversion Actions

```sql
SELECT
  conversion_action.name,
  conversion_action.type,
  conversion_action.category,
  conversion_action.status,
  conversion_action.counting_type,
  conversion_action.attribution_model_settings.attribution_model,
  conversion_action.value_settings.default_value,
  metrics.conversions, metrics.conversions_value
FROM conversion_action
WHERE segments.date DURING LAST_30_DAYS
```

## Conversions by Action (Per Campaign)

```sql
SELECT
  campaign.name,
  segments.conversion_action_name,
  metrics.conversions, metrics.conversions_value,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
  AND metrics.conversions > 0
ORDER BY metrics.conversions DESC
```

## Negative Keywords (Audit Existing)

```sql
SELECT
  campaign.name,
  campaign_criterion.keyword.text,
  campaign_criterion.keyword.match_type,
  campaign_criterion.negative
FROM campaign_criterion
WHERE campaign_criterion.type = 'KEYWORD'
  AND campaign_criterion.negative = TRUE
```

## Negative Keyword Lists (Shared)

```sql
SELECT
  shared_set.name, shared_set.type, shared_set.status,
  shared_set.member_count
FROM shared_set
WHERE shared_set.type = 'NEGATIVE_KEYWORDS'
```

## Period-over-Period Comparison

Run two queries with different date ranges. Calculate:
```
% Change = (period_a - period_b) / period_b * 100
```

Example: Compare last 30 days vs previous 30 days:
```sql
-- Period A: Last 30 days
WHERE segments.date DURING LAST_30_DAYS

-- Period B: Previous 30 days (calculate dates manually)
WHERE segments.date BETWEEN '2026-02-18' AND '2026-03-19'
```

## Budget Utilization (Spend vs Budget)

```sql
SELECT
  campaign.name,
  campaign_budget.amount_micros,
  metrics.cost_micros,
  metrics.clicks, metrics.impressions, metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

Compare `cost_micros` to `amount_micros * 7` (7-day spend vs 7x daily budget) to find budget-capped campaigns.

## Cost Formatting

API returns monetary values in **micros** (1/1,000,000 of currency unit):

| API Value | Display |
|---|---|
| `cost_micros = 1500000` | $1.50 / INR 1.50 |
| `campaign_budget.amount_micros = 50000000` | $50.00/day |
| `cpc_bid_micros = 2500000` | $2.50 |

Always format as currency with 2 decimal places. Check account currency before displaying.
