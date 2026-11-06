import pandas as pd
from pathlib import Path
import re


folder = Path(__file__).resolve().parent



# LOAD YOUR WEEK 1 FINAL FILES

listings = pd.read_csv(
    folder / "combined_listings_residential.csv",
    low_memory=False
)

sold = pd.read_csv(
    folder / "combined_sold_residential.csv",
    low_memory=False
)



print("\n==============================")
print("LISTINGS DATASET")
print("==============================")

print("Rows:", listings.shape[0])
print("Columns:", listings.shape[1])

print("\nFirst 5 rows:")
print(listings.head())

print("\nColumn names:")
print(listings.columns.tolist())

print("\nData types:")
print(listings.dtypes)


print("\n==============================")
print("SOLD DATASET")
print("==============================")

print("Rows:", sold.shape[0])
print("Columns:", sold.shape[1])

print("\nFirst 5 rows:")
print(sold.head())

print("\nColumn names:")
print(sold.columns.tolist())

print("\nData types:")
print(sold.dtypes)


print("\nSTEP 1 COMPLETE!")


# ==================================================
# STEP 2 - MISSING VALUE ANALYSIS
# ==================================================

print("\n\n==============================")
print("LISTINGS - MISSING VALUES")
print("==============================")

listing_missing = pd.DataFrame({
    "Missing_Count": listings.isnull().sum(),
    "Missing_Percent": (
        listings.isnull().sum() / len(listings) * 100
    ).round(2)
})

# Sort from most missing to least missing
listing_missing = listing_missing.sort_values(
    "Missing_Percent",
    ascending=False
)

print(listing_missing)


print("\nLISTINGS - COLUMNS OVER 90% MISSING")

listing_over_90 = listing_missing[
    listing_missing["Missing_Percent"] > 90
]

print(listing_over_90)


print("\n\n==============================")
print("SOLD - MISSING VALUES")
print("==============================")

sold_missing = pd.DataFrame({
    "Missing_Count": sold.isnull().sum(),
    "Missing_Percent": (
        sold.isnull().sum() / len(sold) * 100
    ).round(2)
})

# Sort from most missing to least missing
sold_missing = sold_missing.sort_values(
    "Missing_Percent",
    ascending=False
)

print(sold_missing)


print("\nSOLD - COLUMNS OVER 90% MISSING")

sold_over_90 = sold_missing[
    sold_missing["Missing_Percent"] > 90
]

print(sold_over_90)


print("\nSTEP 2 COMPLETE!")

# ==================================================
# STEP 3 - NUMERIC DISTRIBUTION SUMMARY
# ==================================================

numeric_columns = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]


def numeric_summary(df, dataset_name):

    print("\n\n==============================")
    print(f"{dataset_name} - NUMERIC SUMMARY")
    print("==============================")

    for column in numeric_columns:

        print(f"\n--- {column} ---")

        # Convert to numeric just in case
        values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        print("Count:", values.count())
        print("Missing:", values.isnull().sum())

        print("Minimum:", values.min())
        print("Maximum:", values.max())
        print("Mean:", round(values.mean(), 2))
        print("Median:", values.median())

        print("25th Percentile:", values.quantile(0.25))
        print("50th Percentile:", values.quantile(0.50))
        print("75th Percentile:", values.quantile(0.75))
        print("90th Percentile:", values.quantile(0.90))
        print("95th Percentile:", values.quantile(0.95))
        print("99th Percentile:", values.quantile(0.99))


# Run summary for both datasets
numeric_summary(
    listings,
    "LISTINGS"
)

numeric_summary(
    sold,
    "SOLD"
)


print("\nSTEP 3 COMPLETE!")

# ==================================================
# STEP 4 - HISTOGRAMS AND BOXPLOTS
# ==================================================

import matplotlib.pyplot as plt


def create_plots(df, dataset_name):

    columns = [
        "ClosePrice",
        "LivingArea",
        "DaysOnMarket"
    ]

    for column in columns:

        # Convert values to numeric
        values = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        # ------------------------------------------
        # HISTOGRAM
        # ------------------------------------------

        plt.figure(figsize=(8, 5))

        plt.hist(
            values,
            bins=50
        )

        plt.title(
            f"{dataset_name} - {column} Histogram"
        )

        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()

        histogram_name = (
            f"{dataset_name.lower()}_"
            f"{column.lower()}_histogram.png"
        )

        plt.savefig(
            folder / histogram_name
        )

        plt.close()


        # ------------------------------------------
        # BOXPLOT
        # ------------------------------------------

        plt.figure(figsize=(8, 4))

        plt.boxplot(
            values,
            vert=False
        )

        plt.title(
            f"{dataset_name} - {column} Boxplot"
        )

        plt.xlabel(column)

        plt.tight_layout()

        boxplot_name = (
            f"{dataset_name.lower()}_"
            f"{column.lower()}_boxplot.png"
        )

        plt.savefig(
            folder / boxplot_name
        )

        plt.close()


        print(
            f"Created plots for "
            f"{dataset_name} - {column}"
        )


# Create plots for Listings
create_plots(
    listings,
    "LISTINGS"
)

# Create plots for Sold
create_plots(
    sold,
    "SOLD"
)


print("\nSTEP 4 COMPLETE!")

# ==================================================
# STEP 5 - MORTGAGE RATE ENRICHMENT
# ==================================================

print("\n==============================")
print("STEP 5 - MORTGAGE RATES")
print("==============================")


# ------------------------------------------
# 1. DOWNLOAD FRED MORTGAGE DATA
# ------------------------------------------

fred_url = (
    "https://fred.stlouisfed.org/graph/"
    "fredgraph.csv?id=MORTGAGE30US"
)

mortgage = pd.read_csv(
    fred_url,
    parse_dates=["observation_date"]
)

mortgage.columns = [
    "date",
    "rate_30yr_fixed"
]


# ------------------------------------------
# 2. CONVERT WEEKLY RATES TO MONTHLY AVERAGE
# ------------------------------------------

mortgage["year_month"] = (
    mortgage["date"]
    .dt.to_period("M")
)

mortgage_monthly = (
    mortgage
    .groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)


print("\nMortgage monthly data:")
print(mortgage_monthly.tail())


# ------------------------------------------
# 3. CREATE YEAR-MONTH KEY
# ------------------------------------------

# Sold uses CloseDate
sold["year_month"] = (
    pd.to_datetime(
        sold["CloseDate"],
        errors="coerce"
    )
    .dt.to_period("M")
)

# Listings use ListingContractDate
listings["year_month"] = (
    pd.to_datetime(
        listings["ListingContractDate"],
        errors="coerce"
    )
    .dt.to_period("M")
)


# ------------------------------------------
# 4. MERGE MORTGAGE RATES
# ------------------------------------------

sold_with_rates = sold.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

listings_with_rates = listings.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)


# ------------------------------------------
# 5. VALIDATE THE MERGE
# ------------------------------------------

print("\nSOLD - Missing mortgage rates:")
print(
    sold_with_rates[
        "rate_30yr_fixed"
    ].isnull().sum()
)

print("\nLISTINGS - Missing mortgage rates:")
print(
    listings_with_rates[
        "rate_30yr_fixed"
    ].isnull().sum()
)


print("\nSOLD preview:")
print(
    sold_with_rates[
        [
            "CloseDate",
            "year_month",
            "ClosePrice",
            "rate_30yr_fixed"
        ]
    ].head()
)


print("\nLISTINGS preview:")
print(
    listings_with_rates[
        [
            "ListingContractDate",
            "year_month",
            "ListPrice",
            "rate_30yr_fixed"
        ]
    ].head()
)


# ------------------------------------------
# 6. SAVE ENRICHED DATASETS
# ------------------------------------------

sold_with_rates.to_csv(
    folder / "sold_residential_with_mortgage_rates.csv",
    index=False
)

listings_with_rates.to_csv(
    folder / "listings_residential_with_mortgage_rates.csv",
    index=False
)


print("\nSaved:")
print("sold_residential_with_mortgage_rates.csv")
print("listings_residential_with_mortgage_rates.csv")

print("\nSTEP 5 COMPLETE!")

# ==================================================
# STEP 6 - CHECK UNIQUE PROPERTY TYPES
# ==================================================

print("\n==============================")
print("STEP 6 - UNIQUE PROPERTY TYPES")
print("==============================")


def get_property_types(prefix):

    property_types = set()

    # Find all original monthly files
    files = sorted(folder.glob(f"{prefix}*.csv"))

    # Ignore combined/output files
    files = [
        file for file in files
        if re.search(r"\d{6}", file.name)
    ]

    for file in files:

        df = pd.read_csv(
            file,
            usecols=["PropertyType"],
            low_memory=False
        )

        values = (
            df["PropertyType"]
            .dropna()
            .unique()
        )

        property_types.update(values)

    return sorted(property_types)


listing_property_types = get_property_types(
    "CRMLSListing"
)

sold_property_types = get_property_types(
    "CRMLSSold"
)


print("\nLISTING PROPERTY TYPES FOUND:")
for value in listing_property_types:
    print(value)


print("\nSOLD PROPERTY TYPES FOUND:")
for value in sold_property_types:
    print(value)


print("\nFiltering logic used:")
print(
    'Kept only records where PropertyType == "Residential"'
)


print("\nSTEP 6 COMPLETE!")
