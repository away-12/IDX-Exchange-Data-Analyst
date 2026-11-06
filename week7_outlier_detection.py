import pandas as pd
from pathlib import Path


folder = Path(__file__).resolve().parent


# -----------------------------------------
# LOAD WEEK 6 ENGINEERED SOLD DATA
# -----------------------------------------

sold = pd.read_csv(
    folder / "sold_week6_engineered.csv",
    low_memory=False
)


# -----------------------------------------
# CHECK DATASET
# -----------------------------------------

print("\n==============================")
print("WEEK 7 - STEP 1")
print("==============================")

print("Rows:", len(sold))
print("Columns:", sold.shape[1])


# Check the 3 variables we will use for IQR
print("\nOUTLIER VARIABLES:")

print(
    sold[
        [
            "ClosePrice",
            "LivingArea",
            "DaysOnMarket"
        ]
    ].dtypes
)


print("\nSTEP 1 COMPLETE!")

# ==================================================
# STEP 2 - CALCULATE IQR OUTLIER BOUNDS
# ==================================================

print("\n==============================")
print("STEP 2 - IQR OUTLIER BOUNDS")
print("==============================")


outlier_columns = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]


for column in outlier_columns:

    Q1 = sold[column].quantile(0.25)
    Q3 = sold[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)


    print(f"\n{column}")

    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower Bound:", lower_bound)
    print("Upper Bound:", upper_bound)


print("\nSTEP 2 COMPLETE!")

# ==================================================
# STEP 3 - CREATE OUTLIER FLAGS
# ==================================================

print("\n==============================")
print("STEP 3 - OUTLIER FLAGS")
print("==============================")


outlier_columns = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]


for column in outlier_columns:

    Q1 = sold[column].quantile(0.25)
    Q3 = sold[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)


    flag_column = f"{column}_outlier_flag"


    sold[flag_column] = (
        (sold[column] < lower_bound)
        |
        (sold[column] > upper_bound)
    )


    print(f"\n{column}")
    print(
        "Outliers flagged:",
        sold[flag_column].sum()
    )


# -----------------------------------------
# FLAG IF ROW HAS ANY OUTLIER
# -----------------------------------------

sold["any_outlier_flag"] = (
    sold[
        [
            "ClosePrice_outlier_flag",
            "LivingArea_outlier_flag",
            "DaysOnMarket_outlier_flag"
        ]
    ]
    .any(axis=1)
)


print("\nTOTAL ROWS:", len(sold))

print(
    "ROWS WITH AT LEAST ONE OUTLIER:",
    sold["any_outlier_flag"].sum()
)

print(
    "ROWS WITHOUT OUTLIERS:",
    (~sold["any_outlier_flag"]).sum()
)


print("\nSTEP 3 COMPLETE!")

# ==================================================
# STEP 4 - CREATE FILTERED DATASET AND COMPARE
# ==================================================

print("\n==============================")
print("STEP 4 - FULL VS FILTERED DATA")
print("==============================")


# -----------------------------------------
# CREATE CLEAN FILTERED VERSION
# -----------------------------------------

sold_filtered = sold[
    ~sold["any_outlier_flag"]
].copy()


# -----------------------------------------
# DATASET SIZE COMPARISON
# -----------------------------------------

print("\nDATASET SIZE COMPARISON:")

print("Full dataset rows:", len(sold))
print("Filtered dataset rows:", len(sold_filtered))

print(
    "Rows removed:",
    len(sold) - len(sold_filtered)
)


# -----------------------------------------
# MEDIAN COMPARISON
# -----------------------------------------

print("\nMEDIAN COMPARISON:")

for column in [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]:

    full_median = sold[column].median()

    filtered_median = sold_filtered[column].median()


    print(f"\n{column}")

    print(
        "Full dataset median:",
        full_median
    )

    print(
        "Filtered dataset median:",
        filtered_median
    )


print("\nSTEP 4 COMPLETE!")

# ==================================================
# STEP 5 - SAVE WEEK 7 OUTPUTS
# ==================================================

print("\n==============================")
print("STEP 5 - SAVE OUTPUTS")
print("================================")


# Save full dataset WITH outlier flags
sold.to_csv(
    folder / "sold_week7_with_outlier_flags.csv",
    index=False
)


# Save filtered dataset WITHOUT flagged outliers
sold_filtered.to_csv(
    folder / "sold_week7_filtered.csv",
    index=False
)


print("\nSaved:")
print("sold_week7_with_outlier_flags.csv")
print("sold_week7_filtered.csv")


print("\n")
print("WEEK 7 COMPLETE!")
print("")
