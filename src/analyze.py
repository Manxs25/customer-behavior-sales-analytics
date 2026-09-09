"""Customer Behavior & Sales Analytics Dashboard data pipeline.

This is a new analysis workflow written for the clean project. The source CSV is
treated as input; all transformations, segmentation rules, and summaries are
defined here.
"""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "customer_shopping_behavior.csv"
OUTPUTS = [ROOT / "data", ROOT / "excel_exports", ROOT / "powerbi"]


def snake_case(value: str) -> str:
    return (
        value.strip().lower().replace("(", "").replace(")", "")
        .replace("/", "_").replace(" ", "_").replace("-", "_")
    )


def load_and_clean(path: Path = RAW_PATH) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame.columns = [snake_case(column) for column in frame.columns]

    numeric = [
        "customer_id", "age", "purchase_amount_usd", "review_rating",
        "previous_purchases",
    ]
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame["review_rating"] = frame["review_rating"].fillna(
        frame.groupby("category")["review_rating"].transform("median")
    )
    frame["discount_flag"] = frame["discount_applied"].eq("Yes")
    frame["subscriber_flag"] = frame["subscription_status"].eq("Yes")
    frame["repeat_customer_flag"] = frame["previous_purchases"].ge(10)
    frame["age_band"] = pd.cut(
        frame["age"], bins=[0, 24, 34, 49, 120],
        labels=["Under 25", "25-34", "35-49", "50+"], right=True,
    )
    frequency_days = {
        "Weekly": 7, "Fortnightly": 14, "Monthly": 30,
        "Quarterly": 90, "Every 3 Months": 90, "Bi-Weekly": 14,
    }
    frame["purchase_cycle_days"] = frame["frequency_of_purchases"].map(frequency_days)
    frame["purchase_cycle_days"] = frame["purchase_cycle_days"].fillna(30)
    amount_median = frame["purchase_amount_usd"].median()
    repeat_median = frame["previous_purchases"].median()

    def assign_segment(row: pd.Series) -> str:
        if row["previous_purchases"] >= repeat_median and row["purchase_amount_usd"] >= amount_median:
            return "Loyal high-value"
        if row["subscriber_flag"] and row["previous_purchases"] >= repeat_median:
            return "Subscribed repeat"
        if row["discount_flag"] and row["purchase_amount_usd"] < amount_median:
            return "Promotion-led growth"
        return "New or occasional"

    frame["customer_segment"] = frame.apply(assign_segment, axis=1)
    frame["revenue_per_purchase_day"] = frame["purchase_amount_usd"] / frame["purchase_cycle_days"]
    return frame


def build_outputs(frame: pd.DataFrame) -> None:
    for directory in OUTPUTS:
        directory.mkdir(parents=True, exist_ok=True)

    clean_columns = [
        "customer_id", "age", "age_band", "gender", "item_purchased", "category",
        "purchase_amount_usd", "location", "season", "review_rating",
        "subscription_status", "shipping_type", "discount_applied",
        "previous_purchases", "payment_method", "frequency_of_purchases",
        "discount_flag", "subscriber_flag", "repeat_customer_flag",
        "purchase_cycle_days", "customer_segment", "revenue_per_purchase_day",
    ]
    frame[clean_columns].to_csv(ROOT / "data" / "customer_behavior_clean.csv", index=False)

    category_summary = (
        frame.groupby("category", as_index=False)
        .agg(purchases=("customer_id", "count"), revenue=("purchase_amount_usd", "sum"),
             average_order_value=("purchase_amount_usd", "mean"), average_rating=("review_rating", "mean"))
        .sort_values("revenue", ascending=False)
    )
    segment_summary = (
        frame.groupby("customer_segment", as_index=False)
        .agg(customers=("customer_id", "count"), revenue=("purchase_amount_usd", "sum"),
             average_order_value=("purchase_amount_usd", "mean"), subscriber_rate=("subscriber_flag", "mean"))
        .sort_values("revenue", ascending=False)
    )
    season_summary = (
        frame.groupby("season", as_index=False)
        .agg(revenue=("purchase_amount_usd", "sum"), purchases=("customer_id", "count"))
        .sort_values("revenue", ascending=False)
    )

    kpis = pd.DataFrame([
        {"metric": "Purchases", "value": int(len(frame))},
        {"metric": "Revenue", "value": round(float(frame["purchase_amount_usd"].sum()), 2)},
        {"metric": "Average order value", "value": round(float(frame["purchase_amount_usd"].mean()), 2)},
        {"metric": "Subscriber rate", "value": round(float(frame["subscriber_flag"].mean()), 4)},
        {"metric": "Repeat customer rate", "value": round(float(frame["repeat_customer_flag"].mean()), 4)},
        {"metric": "Average rating", "value": round(float(frame["review_rating"].mean()), 2)},
    ])
    kpis.to_csv(ROOT / "excel_exports" / "kpi_summary.csv", index=False)
    category_summary.to_csv(ROOT / "excel_exports" / "category_summary.csv", index=False)
    segment_summary.to_csv(ROOT / "excel_exports" / "segment_summary.csv", index=False)
    season_summary.to_csv(ROOT / "powerbi" / "season_summary.csv", index=False)
    segment_summary.to_csv(ROOT / "powerbi" / "segment_summary.csv", index=False)
    category_summary.to_csv(ROOT / "powerbi" / "category_summary.csv", index=False)

    top_items = (
        frame.groupby("item_purchased", as_index=False)
        .agg(revenue=("purchase_amount_usd", "sum"), purchases=("customer_id", "count"),
             average_rating=("review_rating", "mean"))
        .sort_values(["revenue", "purchases"], ascending=False).head(10)
    )
    top_items.to_csv(ROOT / "powerbi" / "top_items.csv", index=False)


def main() -> None:
    data = load_and_clean()
    build_outputs(data)
    print(f"Processed {len(data):,} purchases into clean analytics outputs.")


if __name__ == "__main__":
    main()
