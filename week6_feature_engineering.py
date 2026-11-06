import pandas as pd
from pathlib import Path


# -----------------------------------------
# FIND IDX FOLDER
# -----------------------------------------

folder = Path(__file__).resolve().parent


# -----------------------------------------
# LOAD CLEANED DATASETS FROM WEEKS 4-5
# -----------------------------------------

listings = pd.read_csv(
    folder / "listings_cleaned_analysis_ready.csv",
    low_memory=False
)

sold = pd.read_csv(
    folder / "sold_cleaned_analysis_ready.csv",
    low_memory=False
)


# -----------------------------------------
# CHECK THAT FILES LOADED
# -----------------------------------------

print("\n==============================")
print("WEEK 6 - STEP 1")
print("==============================")

print("Listings rows:", len(listings))
print("Listings columns:", listings.shape[1])

print("Sold rows:", len(sold))
print("Sold columns:", sold.shape[1])


print("\nSTEP 1 COMPLETE!")

# ==================================================
# STEP 2 - CREATE YEAR, MONTH, AND YrMo
# ==================================================

print("\n==============================")
print("STEP 2 - TIME VARIABLES")
print("==============================")


# -----------------------------------------
# SOLD DATASET
# Use CloseDate
# -----------------------------------------

sold["CloseDate"] = pd.to_datetime(
    sold["CloseDate"],
    errors="coerce"
)

sold["Year"] = sold["CloseDate"].dt.year

sold["Month"] = sold["CloseDate"].dt.month

sold["YrMo"] = (
    sold["CloseDate"]
    .dt.to_period("M")
    .astype(str)
)


# -----------------------------------------
# LISTINGS DATASET
# Use ListingContractDate
# -----------------------------------------

listings["ListingContractDate"] = pd.to_datetime(
    listings["ListingContractDate"],
    errors="coerce"
)

listings["Year"] = listings[
    "ListingContractDate"
].dt.year

listings["Month"] = listings[
    "ListingContractDate"
].dt.month

listings["YrMo"] = (
    listings["ListingContractDate"]
    .dt.to_period("M")
    .astype(str)
)


# -----------------------------------------
# PREVIEW
# -----------------------------------------

print("\nSOLD PREVIEW:")

print(
    sold[
        [
            "CloseDate",
            "Year",
            "Month",
            "YrMo"
        ]
    ].head()
)


print("\nLISTINGS PREVIEW:")

print(
    listings[
        [
            "ListingContractDate",
            "Year",
            "Month",
            "YrMo"
        ]
    ].head()
)


print("\nSTEP 2 COMPLETE!")

# ==================================================
# STEP 3 - PRICE RATIO METRICS
# ==================================================

print("\n==============================")
print("STEP 3 - PRICE RATIOS")
print("==============================")


# Make sure price columns are numeric
sold["ClosePrice"] = pd.to_numeric(
    sold["ClosePrice"],
    errors="coerce"
)

sold["OriginalListPrice"] = pd.to_numeric(
    sold["OriginalListPrice"],
    errors="coerce"
)


# Avoid division by zero
sold.loc[
    sold["OriginalListPrice"] <= 0,
    "OriginalListPrice"
] = float("nan")


# Price Ratio
sold["PriceRatio"] = (
    sold["ClosePrice"]
    / sold["OriginalListPrice"]
)


# Close-to-Original-List Ratio
sold["CloseToOriginalListRatio"] = (
    sold["ClosePrice"]
    / sold["OriginalListPrice"]
)


# Force ratios to numeric
sold["PriceRatio"] = pd.to_numeric(
    sold["PriceRatio"],
    errors="coerce"
)

sold["CloseToOriginalListRatio"] = pd.to_numeric(
    sold["CloseToOriginalListRatio"],
    errors="coerce"
)


print("\nPRICE RATIO PREVIEW:")

print(
    sold[
        [
            "OriginalListPrice",
            "ClosePrice",
            "PriceRatio",
            "CloseToOriginalListRatio"
        ]
    ].head(10)
)


print("\nPRICE RATIO TYPES:")

print(
    sold[
        [
            "PriceRatio",
            "CloseToOriginalListRatio"
        ]
    ].dtypes
)


print("\nPRICE RATIO SUMMARY:")

print(
    sold[
        [
            "PriceRatio",
            "CloseToOriginalListRatio"
        ]
    ].describe()
)


print("\nSTEP 3 COMPLETE!")

# ==================================================
# STEP 4 - PRICE PER SQUARE FOOT
# ==================================================

print("\n==============================")
print("STEP 4 - PRICE PER SQ FT")
print("==============================")


# Make sure LivingArea is numeric
sold["LivingArea"] = pd.to_numeric(
    sold["LivingArea"],
    errors="coerce"
)


# -----------------------------------------
# CREATE PRICE PER SQUARE FOOT
# -----------------------------------------

sold["PricePerSqFt"] = (
    sold["ClosePrice"]
    / sold["LivingArea"]
)


# -----------------------------------------
# MAKE SURE RESULT IS NUMERIC
# -----------------------------------------

sold["PricePerSqFt"] = pd.to_numeric(
    sold["PricePerSqFt"],
    errors="coerce"
)


# -----------------------------------------
# PREVIEW
# -----------------------------------------

print("\nPRICE PER SQ FT PREVIEW:")

print(
    sold[
        [
            "ClosePrice",
            "LivingArea",
            "PricePerSqFt"
        ]
    ].head(10)
)


# -----------------------------------------
# SUMMARY
# -----------------------------------------

print("\nPRICE PER SQ FT SUMMARY:")

print(
    sold["PricePerSqFt"].describe()
)


print("\nSTEP 4 COMPLETE!")

# ==================================================
# STEP 5 - TRANSACTION TIMELINE METRICS
# ==================================================

print("\n==============================")
print("STEP 5 - TIMELINE METRICS")
print("==============================")


# -----------------------------------------
# CONVERT DATES TO DATETIME
# -----------------------------------------

sold["ListingContractDate"] = pd.to_datetime(
    sold["ListingContractDate"],
    errors="coerce"
)

sold["PurchaseContractDate"] = pd.to_datetime(
    sold["PurchaseContractDate"],
    errors="coerce"
)

sold["CloseDate"] = pd.to_datetime(
    sold["CloseDate"],
    errors="coerce"
)


# -----------------------------------------
# LISTING TO CONTRACT DAYS
# -----------------------------------------

sold["ListingToContractDays"] = (
    sold["PurchaseContractDate"]
    - sold["ListingContractDate"]
).dt.days


# -----------------------------------------
# CONTRACT TO CLOSE DAYS
# -----------------------------------------

sold["ContractToCloseDays"] = (
    sold["CloseDate"]
    - sold["PurchaseContractDate"]
).dt.days


# -----------------------------------------
# PREVIEW
# -----------------------------------------

print("\nTIMELINE PREVIEW:")

print(
    sold[
        [
            "ListingContractDate",
            "PurchaseContractDate",
            "CloseDate",
            "ListingToContractDays",
            "ContractToCloseDays"
        ]
    ].head(10)
)


# -----------------------------------------
# SUMMARY
# -----------------------------------------

print("\nLISTING TO CONTRACT SUMMARY:")
print(
    sold["ListingToContractDays"].describe()
)

print("\nCONTRACT TO CLOSE SUMMARY:")
print(
    sold["ContractToCloseDays"].describe()
)


print("\nSTEP 5 COMPLETE!")

# ==================================================
# STEP 6 - SEGMENTED SUMMARY BY COUNTY
# ==================================================

print("\n==============================")
print("STEP 6 - COUNTY SUMMARY")
print("==============================")


county_summary = (
    sold
    .groupby("CountyOrParish")
    .agg(
        HomesSold=("ListingKey", "count"),
        MedianClosePrice=("ClosePrice", "median"),
        AverageClosePrice=("ClosePrice", "mean"),
        AverageDaysOnMarket=("DaysOnMarket", "mean"),
        MedianPricePerSqFt=("PricePerSqFt", "median"),
        AveragePriceRatio=("PriceRatio", "mean")
    )
    .reset_index()
)


# Sort counties by number of homes sold
county_summary = county_summary.sort_values(
    "HomesSold",
    ascending=False
)


print("\nCOUNTY SUMMARY:")
print(
    county_summary.head(15).to_string(index=False)
)


print("\nSTEP 6 COMPLETE!")

# ==================================================
# STEP 7 - FINAL WEEK 6 CHECK AND SAVE
# ==================================================

print("\n==============================")
print("STEP 7 - FINAL WEEK 6 OUTPUT")
print("==============================")


# -----------------------------------------
# REQUIRED ENGINEERED COLUMNS
# -----------------------------------------

required_sold_columns = [
    "PriceRatio",
    "CloseToOriginalListRatio",
    "PricePerSqFt",
    "DaysOnMarket",
    "Year",
    "Month",
    "YrMo",
    "ListingToContractDays",
    "ContractToCloseDays"
]

required_listing_columns = [
    "Year",
    "Month",
    "YrMo"
]


# -----------------------------------------
# CHECK SOLD COLUMNS
# -----------------------------------------

print("\nSOLD - REQUIRED COLUMNS CHECK")

for column in required_sold_columns:

    if column in sold.columns:
        print(f"{column}: OK")

    else:
        print(f"{column}: MISSING")


# -----------------------------------------
# CHECK LISTINGS COLUMNS
# -----------------------------------------

print("\nLISTINGS - REQUIRED COLUMNS CHECK")

for column in required_listing_columns:

    if column in listings.columns:
        print(f"{column}: OK")

    else:
        print(f"{column}: MISSING")


# -----------------------------------------
# SAMPLE OUTPUT TABLE
# -----------------------------------------

print("\nSAMPLE ENGINEERED SOLD DATA:")

sample_columns = [
    "ListingKey",
    "ClosePrice",
    "OriginalListPrice",
    "LivingArea",
    "DaysOnMarket",
    "YrMo",
    "PriceRatio",
    "CloseToOriginalListRatio",
    "PricePerSqFt",
    "ListingToContractDays",
    "ContractToCloseDays"
]

print(
    sold[
        sample_columns
    ].head(10).to_string(index=False)
)


# -----------------------------------------
# SAVE ENGINEERED DATASETS
# -----------------------------------------

sold.to_csv(
    folder / "sold_week6_engineered.csv",
    index=False
)

listings.to_csv(
    folder / "listings_week6_engineered.csv",
    index=False
)


# Save county summary too
county_summary.to_csv(
    folder / "week6_county_summary.csv",
    index=False
)


print("\nSaved:")
print("sold_week6_engineered.csv")
print("listings_week6_engineered.csv")
print("week6_county_summary.csv")


print("\n==============================")
print("WEEK 6 COMPLETE!")
print("==============================")