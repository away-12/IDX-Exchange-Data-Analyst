import pandas as pd
from pathlib import Path
import re


# --------------------------------------------------
# 1. FIND THE IDX FOLDER
# --------------------------------------------------

# This Python file should be saved inside your IDX folder
folder = Path(__file__).resolve().parent


# --------------------------------------------------
# 2. MONTHS REQUIRED FOR WEEK 1
# January 2024 through August 2026 = 32 months
# --------------------------------------------------

expected_months = [
    period.strftime("%Y%m")
    for period in pd.period_range(
        start="2024-01",
        end="2026-08",
        freq="M"
    )
]


# --------------------------------------------------
# 3. FIND ONE FILE FOR EACH MONTH
# --------------------------------------------------

def get_monthly_files(prefix):

    monthly_files = {}

    # Look at all CSV files in the IDX folder
    for file in folder.glob("*.csv"):

        # Only accept actual monthly files like:
        # CRMLSListing202401.csv
        # CRMLSListing202401_filled.csv
        # CRMLSSold202401.csv
        pattern = rf"^{re.escape(prefix)}(\d{{6}})(?:_filled)?\.csv$"

        match = re.match(pattern, file.name)

        if not match:
            continue

        month = match.group(1)

        # Only use Jan 2024 through Aug 2026
        if month not in expected_months:
            continue

        # First file found for this month
        if month not in monthly_files:
            monthly_files[month] = file

        # Prefer a _filled version if one exists
        elif "_filled" in file.name:
            monthly_files[month] = file


    # --------------------------------------------------
    # CHECK FOR MISSING MONTHS
    # --------------------------------------------------

    missing_months = [
        month
        for month in expected_months
        if month not in monthly_files
    ]

    if missing_months:

        print("\nERROR: Missing monthly files!")

        for month in missing_months:
            print(month)

        raise ValueError(
            f"{prefix} is missing {len(missing_months)} month(s)."
        )


    # Return files in chronological order
    return [
        monthly_files[month]
        for month in expected_months
    ]


# --------------------------------------------------
# 4. COMBINE AND FILTER DATA
# --------------------------------------------------

def combine_files(prefix, output_name):

    files = get_monthly_files(prefix)

    print("\n======================================")
    print(f"PROCESSING {prefix}")
    print("======================================")

    print(f"Files loaded: {len(files)}")

    dataframes = []

    total_rows_before_concat = 0


    # --------------------------------------------------
    # READ EVERY MONTH
    # --------------------------------------------------

    for file in files:

        print(f"Reading: {file.name}")

        df = pd.read_csv(
            file,
            low_memory=False
        )

        total_rows_before_concat += len(df)

        dataframes.append(df)


    # --------------------------------------------------
    # 5. CONCATENATE ALL MONTHS
    # --------------------------------------------------

    combined = pd.concat(
        dataframes,
        ignore_index=True
    )


    print("\nROW COUNT CHECK - CONCATENATION")

    print(
        "Rows before concatenation:",
        total_rows_before_concat
    )

    print(
        "Rows after concatenation:",
        len(combined)
    )


    # Make sure no rows disappeared during concatenation
    if total_rows_before_concat != len(combined):

        raise ValueError(
            "Row counts do not match after concatenation!"
        )


    # --------------------------------------------------
    # 6. FILTER TO RESIDENTIAL ONLY
    # --------------------------------------------------

    rows_before_filter = len(combined)

    residential = combined[
        combined["PropertyType"] == "Residential"
    ].copy()

    rows_after_filter = len(residential)

    rows_removed = (
        rows_before_filter
        - rows_after_filter
    )


    print("\nROW COUNT CHECK - RESIDENTIAL FILTER")

    print(
        "Rows before Residential filter:",
        rows_before_filter
    )

    print(
        "Rows after Residential filter:",
        rows_after_filter
    )

    print(
        "Rows removed:",
        rows_removed
    )


    # --------------------------------------------------
    # 7. SAVE FINAL CSV
    # --------------------------------------------------

    output_path = folder / output_name

    residential.to_csv(
        output_path,
        index=False
    )

    print("\nSaved:")
    print(output_path)

    print("======================================")


# --------------------------------------------------
# 8. PROCESS LISTING DATA
# --------------------------------------------------

combine_files(
    "CRMLSListing",
    "combined_listings_residential.csv"
)


# --------------------------------------------------
# 9. PROCESS SOLD DATA
# --------------------------------------------------

combine_files(
    "CRMLSSold",
    "combined_sold_residential.csv"
)


# --------------------------------------------------
# 10. FINISHED
# --------------------------------------------------

print("\n======================================")
print("WEEK 1 COMPLETE!")
print("======================================")