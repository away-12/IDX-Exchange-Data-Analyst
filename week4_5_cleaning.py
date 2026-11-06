import pandas as pd
from pathlib import Path


# -----------------------------------------
# FIND IDX FOLDER
# -----------------------------------------

folder = Path(__file__).resolve().parent


# -----------------------------------------
# LOAD WEEK 2-3 ENRICHED FILES
# -----------------------------------------

listings = pd.read_csv(
    folder / "listings_residential_with_mortgage_rates.csv",
    low_memory=False
)

sold = pd.read_csv(
    folder / "sold_residential_with_mortgage_rates.csv",
    low_memory=False
)


# -----------------------------------------
# CHECK STARTING ROW COUNTS
# -----------------------------------------

print("\n==============================")
print("STARTING DATASET SIZE")
print("==============================")

print("Listings rows:", len(listings))
print("Listings columns:", listings.shape[1])

print("Sold rows:", len(sold))
print("Sold columns:", sold.shape[1])


print("\nSTEP 1 COMPLETE!")

# ==================================================
# STEP 2 - CONVERT DATE COLUMNS TO DATETIME
# ==================================================

print("\n==============================")
print("STEP 2 - DATE CONVERSION")
print("==============================")


date_columns = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]


# -----------------------------------------
# CONVERT LISTINGS DATES
# -----------------------------------------

for column in date_columns:

    if column in listings.columns:

        listings[column] = pd.to_datetime(
            listings[column],
            errors="coerce"
        )


# -----------------------------------------
# CONVERT SOLD DATES
# -----------------------------------------

for column in date_columns:

    if column in sold.columns:

        sold[column] = pd.to_datetime(
            sold[column],
            errors="coerce"
        )


# -----------------------------------------
# CONFIRM DATA TYPES
# -----------------------------------------

print("\nLISTINGS DATE TYPES:")

for column in date_columns:

    print(
        column,
        listings[column].dtype
    )


print("\nSOLD DATE TYPES:")

for column in date_columns:

    print(
        column,
        sold[column].dtype
    )


# -----------------------------------------
# CHECK MISSING DATES AFTER CONVERSION
# -----------------------------------------

print("\nLISTINGS - MISSING DATES:")

for column in date_columns:

    print(
        column,
        listings[column].isnull().sum()
    )


print("\nSOLD - MISSING DATES:")

for column in date_columns:

    print(
        column,
        sold[column].isnull().sum()
    )


print("\nSTEP 2 COMPLETE!")

# ==================================================
# STEP 3 - NUMERIC TYPE CHECKS AND INVALID VALUES
# ==================================================

print("\n==============================")
print("STEP 3 - NUMERIC VALIDATION")
print("==============================")


numeric_columns = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket",
    "BedroomsTotal",
    "BathroomsTotalInteger"
]


# -----------------------------------------
# CONVERT TO NUMERIC
# -----------------------------------------

for column in numeric_columns:

    if column in listings.columns:
        listings[column] = pd.to_numeric(
            listings[column],
            errors="coerce"
        )

    if column in sold.columns:
        sold[column] = pd.to_numeric(
            sold[column],
            errors="coerce"
        )


# -----------------------------------------
# CONFIRM DATA TYPES
# -----------------------------------------

print("\nLISTINGS NUMERIC TYPES:")

for column in numeric_columns:
    print(column, listings[column].dtype)


print("\nSOLD NUMERIC TYPES:")

for column in numeric_columns:
    print(column, sold[column].dtype)


# -----------------------------------------
# INVALID VALUE COUNTS - LISTINGS
# -----------------------------------------

print("\nLISTINGS - INVALID VALUES")

print(
    "ClosePrice <= 0:",
    (listings["ClosePrice"] <= 0).sum()
)

print(
    "LivingArea <= 0:",
    (listings["LivingArea"] <= 0).sum()
)

print(
    "DaysOnMarket < 0:",
    (listings["DaysOnMarket"] < 0).sum()
)

print(
    "BedroomsTotal < 0:",
    (listings["BedroomsTotal"] < 0).sum()
)

print(
    "BathroomsTotalInteger < 0:",
    (listings["BathroomsTotalInteger"] < 0).sum()
)


# -----------------------------------------
# INVALID VALUE COUNTS - SOLD
# -----------------------------------------

print("\nSOLD - INVALID VALUES")

print(
    "ClosePrice <= 0:",
    (sold["ClosePrice"] <= 0).sum()
)

print(
    "LivingArea <= 0:",
    (sold["LivingArea"] <= 0).sum()
)

print(
    "DaysOnMarket < 0:",
    (sold["DaysOnMarket"] < 0).sum()
)

print(
    "BedroomsTotal < 0:",
    (sold["BedroomsTotal"] < 0).sum()
)

print(
    "BathroomsTotalInteger < 0:",
    (sold["BathroomsTotalInteger"] < 0).sum()
)


print("\nSTEP 3 COMPLETE!")

# ==================================================
# STEP 4 - DATE CONSISTENCY CHECKS
# ==================================================

print("\n==============================")
print("STEP 4 - DATE CONSISTENCY")
print("==============================")


def add_date_flags(df, dataset_name):

    # Listing date should NOT be after close date
    df["listing_after_close_flag"] = (
        df["ListingContractDate"].notna()
        & df["CloseDate"].notna()
        & (df["ListingContractDate"] > df["CloseDate"])
    )

    # Purchase contract date should NOT be after close date
    df["purchase_after_close_flag"] = (
        df["PurchaseContractDate"].notna()
        & df["CloseDate"].notna()
        & (df["PurchaseContractDate"] > df["CloseDate"])
    )

    # Purchase contract date should NOT be before listing date
    df["negative_timeline_flag"] = (
        df["ListingContractDate"].notna()
        & df["PurchaseContractDate"].notna()
        & (df["PurchaseContractDate"] < df["ListingContractDate"])
    )

    print(f"\n{dataset_name} - DATE FLAG COUNTS")

    print(
        "listing_after_close_flag:",
        df["listing_after_close_flag"].sum()
    )

    print(
        "purchase_after_close_flag:",
        df["purchase_after_close_flag"].sum()
    )

    print(
        "negative_timeline_flag:",
        df["negative_timeline_flag"].sum()
    )


# Apply to both datasets
add_date_flags(
    listings,
    "LISTINGS"
)

add_date_flags(
    sold,
    "SOLD"
)


print("\nSTEP 4 COMPLETE!")

# ==================================================
# STEP 5 - GEOGRAPHIC DATA QUALITY CHECKS
# ==================================================

print("\n==============================")
print("STEP 5 - GEOGRAPHIC CHECKS")
print("==============================")


def geographic_checks(df, dataset_name):

    # Make sure coordinates are numeric
    df["Latitude"] = pd.to_numeric(
        df["Latitude"],
        errors="coerce"
    )

    df["Longitude"] = pd.to_numeric(
        df["Longitude"],
        errors="coerce"
    )

    print(f"\n{dataset_name} - GEOGRAPHIC CHECKS")

    # Missing coordinates
    missing_lat = df["Latitude"].isnull().sum()
    missing_lon = df["Longitude"].isnull().sum()

    print("Missing Latitude:", missing_lat)
    print("Missing Longitude:", missing_lon)

    # Zero coordinates
    lat_zero = (df["Latitude"] == 0).sum()
    lon_zero = (df["Longitude"] == 0).sum()

    print("Latitude = 0:", lat_zero)
    print("Longitude = 0:", lon_zero)

    # California longitude should be negative
    positive_longitude = (df["Longitude"] > 0).sum()

    print("Longitude > 0:", positive_longitude)

    # Rough California coordinate bounds
    implausible_coordinates = (
        (df["Latitude"] < 32)
        | (df["Latitude"] > 42)
        | (df["Longitude"] < -125)
        | (df["Longitude"] > -114)
    )

    print(
        "Implausible / out-of-state coordinates:",
        implausible_coordinates.sum()
    )


# Run checks
geographic_checks(
    listings,
    "LISTINGS"
)

geographic_checks(
    sold,
    "SOLD"
)


print("\nSTEP 5 COMPLETE!")

# ==================================================
# STEP 6 - CHECK REDUNDANT DUPLICATE COLUMNS
# ==================================================

print("\n==============================")
print("STEP 6 - DUPLICATE COLUMN CHECK")
print("==============================")


duplicate_pairs = [
    ("PropertyType", "PropertyType.1"),
    ("ListAgentFirstName", "ListAgentFirstName.1"),
    ("DaysOnMarket", "DaysOnMarket.1"),
    ("LivingArea", "LivingArea.1"),
    ("Longitude", "Longitude.1"),
    ("Latitude", "Latitude.1"),
    ("ListPrice", "ListPrice.1"),
    ("ListAgentLastName", "ListAgentLastName.1"),
    ("CloseDate", "CloseDate.1"),
    ("BuyerOfficeName", "BuyerOfficeName.1"),
    ("UnparsedAddress", "UnparsedAddress.1")
]


print("\nLISTINGS - DUPLICATE COLUMN COMPARISON")

for original, duplicate in duplicate_pairs:

    if (
        original in listings.columns
        and duplicate in listings.columns
    ):

        same_values = (
            listings[original]
            .fillna("__MISSING__")
            .astype(str)
            ==
            listings[duplicate]
            .fillna("__MISSING__")
            .astype(str)
        )

        different_count = (~same_values).sum()

        print(
            f"{original} vs {duplicate}: "
            f"{different_count} different rows"
        )


print("\nSTEP 6 COMPLETE!")

# ==================================================
# STEP 7 - INVESTIGATE NON-IDENTICAL DUPLICATE COLUMNS
# ==================================================

print("\n==============================")
print("STEP 7 - INVESTIGATE DUPLICATES")
print("==============================")


check_pairs = [
    ("CloseDate", "CloseDate.1"),
    ("BuyerOfficeName", "BuyerOfficeName.1"),
    ("UnparsedAddress", "UnparsedAddress.1")
]


for original, duplicate in check_pairs:

    print(f"\n--- {original} vs {duplicate} ---")

    print(
        f"{original} missing:",
        listings[original].isnull().sum()
    )

    print(
        f"{duplicate} missing:",
        listings[duplicate].isnull().sum()
    )

    # Rows where values differ
    different = listings[
        listings[original].fillna("__MISSING__").astype(str)
        !=
        listings[duplicate].fillna("__MISSING__").astype(str)
    ]

    print(
        "Different rows:",
        len(different)
    )

    print("\nSample differences:")

    print(
        different[
            [original, duplicate]
        ].head(10)
    )


print("\nSTEP 7 COMPLETE!")

# ==================================================
# STEP 8 - VERIFY CLOSEDATE DUPLICATE
# ==================================================

print("\n==============================")
print("STEP 8 - VERIFY CLOSEDATE")
print("==============================")


# Convert the duplicate CloseDate column to datetime
listings["CloseDate.1"] = pd.to_datetime(
    listings["CloseDate.1"],
    errors="coerce"
)


# Compare again
close_date_different = (
    listings["CloseDate"].fillna(pd.Timestamp("1900-01-01"))
    !=
    listings["CloseDate.1"].fillna(pd.Timestamp("1900-01-01"))
)


print(
    "CloseDate differences after datetime conversion:",
    close_date_different.sum()
)


print("\nSTEP 8 COMPLETE!")

# ==================================================
# STEP 9 - FINAL CLEANING AND SAVE
# ==================================================

print("\n==============================")
print("STEP 9 - FINAL CLEANING")
print("==============================")


# --------------------------------------------------
# 1. SAVE STARTING ROW COUNTS
# --------------------------------------------------

listings_start_rows = len(listings)
sold_start_rows = len(sold)


# --------------------------------------------------
# 2. REMOVE CONFIRMED REDUNDANT COLUMNS
# --------------------------------------------------

duplicate_columns = [
    "PropertyType.1",
    "ListAgentFirstName.1",
    "DaysOnMarket.1",
    "LivingArea.1",
    "Longitude.1",
    "Latitude.1",
    "ListPrice.1",
    "ListAgentLastName.1",
    "CloseDate.1",
    "BuyerOfficeName.1",
    "UnparsedAddress.1"
]

listings = listings.drop(
    columns=[
        col for col in duplicate_columns
        if col in listings.columns
    ]
)


# --------------------------------------------------
# 3. CREATE INVALID NUMERIC FLAGS
# --------------------------------------------------

listings["invalid_numeric_flag"] = (
    (listings["LivingArea"] <= 0)
    | (listings["DaysOnMarket"] < 0)
    | (listings["BedroomsTotal"] < 0)
    | (listings["BathroomsTotalInteger"] < 0)
    | (
        listings["ClosePrice"].notna()
        & (listings["ClosePrice"] <= 0)
    )
)

sold["invalid_numeric_flag"] = (
    (sold["ClosePrice"] <= 0)
    | (sold["LivingArea"] <= 0)
    | (sold["DaysOnMarket"] < 0)
    | (sold["BedroomsTotal"] < 0)
    | (sold["BathroomsTotalInteger"] < 0)
)


# --------------------------------------------------
# 4. CREATE GEOGRAPHIC QUALITY FLAG
# --------------------------------------------------

listings["geographic_issue_flag"] = (
    listings["Latitude"].isna()
    | listings["Longitude"].isna()
    | (listings["Latitude"] == 0)
    | (listings["Longitude"] == 0)
    | (listings["Longitude"] > 0)
    | (listings["Latitude"] < 32)
    | (listings["Latitude"] > 42)
    | (listings["Longitude"] < -125)
    | (listings["Longitude"] > -114)
)

sold["geographic_issue_flag"] = (
    sold["Latitude"].isna()
    | sold["Longitude"].isna()
    | (sold["Latitude"] == 0)
    | (sold["Longitude"] == 0)
    | (sold["Longitude"] > 0)
    | (sold["Latitude"] < 32)
    | (sold["Latitude"] > 42)
    | (sold["Longitude"] < -125)
    | (sold["Longitude"] > -114)
)


# --------------------------------------------------
# 5. CREATE CLEAN ANALYSIS DATASETS
# Remove only invalid numeric records
#
# Keep date/geographic problems as FLAGGED records
# instead of deleting them.
# --------------------------------------------------

listings_clean = listings[
    ~listings["invalid_numeric_flag"]
].copy()

sold_clean = sold[
    ~sold["invalid_numeric_flag"]
].copy()


# --------------------------------------------------
# 6. FINAL ROW COUNTS
# --------------------------------------------------

print("\nLISTINGS")

print(
    "Rows before cleaning:",
    listings_start_rows
)

print(
    "Invalid numeric rows removed:",
    listings["invalid_numeric_flag"].sum()
)

print(
    "Rows after cleaning:",
    len(listings_clean)
)

print(
    "Date issue rows:",
    (
        listings[
            [
                "listing_after_close_flag",
                "purchase_after_close_flag",
                "negative_timeline_flag"
            ]
        ].any(axis=1)
    ).sum()
)

print(
    "Geographic issue rows:",
    listings["geographic_issue_flag"].sum()
)


print("\nSOLD")

print(
    "Rows before cleaning:",
    sold_start_rows
)

print(
    "Invalid numeric rows removed:",
    sold["invalid_numeric_flag"].sum()
)

print(
    "Rows after cleaning:",
    len(sold_clean)
)

print(
    "Date issue rows:",
    (
        sold[
            [
                "listing_after_close_flag",
                "purchase_after_close_flag",
                "negative_timeline_flag"
            ]
        ].any(axis=1)
    ).sum()
)

print(
    "Geographic issue rows:",
    sold["geographic_issue_flag"].sum()
)


# --------------------------------------------------
# 7. SAVE CLEANED DATASETS
# --------------------------------------------------

listings_clean.to_csv(
    folder / "listings_cleaned_analysis_ready.csv",
    index=False
)

sold_clean.to_csv(
    folder / "sold_cleaned_analysis_ready.csv",
    index=False
)


print("\nSaved:")
print("listings_cleaned_analysis_ready.csv")
print("sold_cleaned_analysis_ready.csv")

print("\nWEEKS 4-5 COMPLETE!")

