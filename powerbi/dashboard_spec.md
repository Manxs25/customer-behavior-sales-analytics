# Power BI Dashboard Specification

The Power BI layer is designed as a new three-page report using the generated CSVs in this folder.

## Page 1: Executive Pulse

- KPI cards: Revenue, purchases, average order value, subscriber rate, repeat customer rate.
- Column chart: revenue by category.
- Bar chart: revenue by season.
- Slicer: season, category, subscription status.

## Page 2: Customer Growth

- Stacked bar: revenue by `customer_segment`.
- Scatter plot: previous purchases versus purchase amount, colored by segment.
- Matrix: segment, customers, revenue, average order value, subscriber rate.
- Slicer: age band, gender, discount flag.

## Page 3: Offer and Experience

- Bar chart: average order value by shipping type.
- Heatmap: category by age band using revenue.
- Table: top items by revenue, purchase count, and average rating.
- Slicer: payment method and season.

## Model

Load `data/customer_behavior_clean.csv` as the transaction fact table. Use the generated
summary CSVs for fast KPI validation and export-ready Excel views. Format revenue and
average order value as currency, rates as percentages, and ratings to one decimal place.
