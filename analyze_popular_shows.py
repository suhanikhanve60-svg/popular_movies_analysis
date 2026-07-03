"""
Case study analysis: popular_shows_dataset.csv
Audits for duplication issues, then produces a clean revenue ranking.
"""

import pandas as pd

# ---- 1. Load ----
df = pd.read_csv("popular_shows_dataset.csv")

print(f"Total rows: {len(df)}")
print(f"Unique titles: {df['title'].nunique()}")
print()

# ---- 2. Data quality audit ----
print("Rows per title:")
print(df["title"].value_counts())
print()

fully_duplicated = df.duplicated().sum()
print(f"Fully duplicated rows: {fully_duplicated} out of {len(df)} "
      f"({fully_duplicated / len(df):.0%})")
print()

print("Missing values per column:")
print(df.isnull().sum())
print()

# ---- 3. Deduplicate to unique records ----
clean = df.drop_duplicates(subset="title").copy()
clean["revenue_musd"] = clean["revenue"] / 1e6
clean = clean.sort_values("revenue", ascending=False)

print("Clean, deduplicated revenue ranking:")
print(clean[["title", "year", "revenue_musd"]].to_string(index=False))
print()

# ---- 4. Summary stats ----
total_revenue = clean["revenue"].sum()
top2_share = clean["revenue"].iloc[:2].sum() / total_revenue

print(f"Total combined revenue (10 unique titles): ${total_revenue:,.0f}")
print(f"Top 2 titles' share of total revenue: {top2_share:.0%}")
print()

print("Year distribution (unique titles):")
print(clean["year"].value_counts().sort_index())

# ---- 5. Save cleaned data ----
clean.to_csv("popular_shows_dataset_clean.csv", index=False)
print("\nSaved deduplicated dataset to popular_shows_dataset_clean.csv")
