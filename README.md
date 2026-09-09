# Customer Behavior & Sales Analytics Dashboard

An original analytics project that turns customer shopping transactions into practical sales and retention decisions. The project uses the supplied CSV only as input and implements a new cleaning workflow, segmentation method, business-question set, SQL analysis, Excel-ready exports, and Power BI report design.

## What this project answers

- Which product categories and seasons drive revenue?
- How do subscribers compare with non-subscribers on order value and repeat behavior?
- Which customer groups need retention, value, or promotion-led messaging?
- Are shipping choices associated with larger baskets or better ratings?
- Which age bands and products offer the clearest growth opportunities?

## Stack

Python, Pandas, NumPy, SQL, Power BI, and Microsoft Excel.

## Project layout

```text
customer-behavior-sales-analytics/
|-- data/
|   |-- customer_shopping_behavior.csv
|   `-- customer_behavior_clean.csv       # generated
|-- excel_exports/                        # Excel-compatible CSV views
|-- powerbi/                              # Power BI inputs and report design
|-- sql/analysis_queries.sql
|-- src/analyze.py
|-- LICENSE
|-- THIRD_PARTY_NOTICES.md
`-- README.md
```

## Methodology

The Python pipeline standardizes column names, coerces numeric fields, imputes missing review ratings using the median for each category, adds age bands, converts purchase frequency to a day-based cycle, and creates flags for discounts, subscriptions, and repeat behavior.

The segmentation model is intentionally transparent:

- **Loyal high-value:** above-median prior purchases and order value.
- **Subscribed repeat:** subscriber with above-median prior purchases.
- **Promotion-led growth:** discount user with below-median order value.
- **New or occasional:** remaining customers.

This is a behavioral grouping for marketing analysis, not a claim about individual identity or lifetime value.

## Run locally

```powershell
python -m pip install -r requirements.txt
python src/analyze.py
```

The command writes cleaned data, Excel-ready summaries, and Power BI input tables. SQL examples assume the cleaned CSV has been loaded into a table named `customer_behavior_clean`.

## Dashboard

`powerbi/dashboard_spec.md` defines the original three-page Power BI design: Executive Pulse, Customer Growth, and Offer and Experience. The generated CSVs in `powerbi/` are ready to import into Power BI.

## Initial findings and actions

The first pipeline run covers 3,900 purchases, $233,081 in revenue, a $59.76 average order value, a 27.0% subscriber rate, and an 81.9% repeat-customer rate.

- Clothing contributes the largest revenue pool, while Footwear has the strongest average rating and order value; merchandise planning should protect Clothing volume while testing Footwear cross-sells.
- Loyal high-value customers represent about 26% of purchases but generate roughly 35% of revenue at an $80.27 average order value; prioritize retention benefits and early-access offers for this group.
- Promotion-led growth customers have a $38.78 average order value and a 42.5% subscriber rate; test subscription bundles that reward a second purchase without broad discounting.
- Fall is the highest-revenue season in this dataset; plan inventory and campaign capacity ahead of Fall while using Spring as a close second.

These findings are descriptive signals from the supplied transaction sample, not causal claims.

## License and attribution

The original implementation in this repository is new. The source dataset is retained under the applicable notice in `THIRD_PARTY_NOTICES.md`; that notice must remain with redistributed copies of the dataset. See `LICENSE` for the license covering the new project files.
