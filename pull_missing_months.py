
from pathlib import Path
import subprocess
import sys


# LOCATION OF YOUR IDX FOLDER

folder = Path(__file__).resolve().parent

listed_script = folder / "crmls_listed.py"
sold_script = folder / "crmls_sold.py"


# --------------------------------------------------
# MONTHS WE NEED
# --------------------------------------------------

months = [
    (5, 6, "202605"),   # May
    (6, 7, "202606"),   # June
    (7, 8, "202607"),   # July
    (8, 9, "202608")    # August
]


# --------------------------------------------------
# FUNCTION TO RUN LISTING SCRIPT
# --------------------------------------------------

def run_listing_month(month, next_month, yyyymm):

    print("\n==============================================")
    print(f"DOWNLOADING LISTINGS FOR {yyyymm}")
    print("==============================================")

    # Read your ORIGINAL provided script
    code = listed_script.read_text()

    # Replace February start date
    code = code.replace(
        "datetime(2026, 2, 1)",
        f"datetime(2026, {month}, 1)"
    )

    # Replace March end date
    code = code.replace(
        "datetime(2026, 3, 1)",
        f"datetime(2026, {next_month}, 1)"
    )

    # Replace output filename
    code = code.replace(
        "CRMLSListing202602.csv",
        f"CRMLSListing{yyyymm}.csv"
    )

    # Create temporary script
    temp_script = folder / "_temp_listing.py"

    temp_script.write_text(code)

    # Run temporary script
    subprocess.run(
        [sys.executable, str(temp_script)],
        cwd=folder,
        check=True
    )

    # Delete temporary script
    temp_script.unlink()

    print(f"FINISHED LISTINGS {yyyymm}")


# --------------------------------------------------
# FUNCTION TO RUN SOLD SCRIPT
# --------------------------------------------------

def run_sold_month(month, next_month, yyyymm):

    print("\n==============================================")
    print(f"DOWNLOADING SOLD DATA FOR {yyyymm}")
    print("==============================================")

    # Read your ORIGINAL provided script
    code = sold_script.read_text()

    # Replace February start date
    code = code.replace(
        "datetime(2026, 2, 1)",
        f"datetime(2026, {month}, 1)"
    )

    # Replace March end date
    code = code.replace(
        "datetime(2026, 3, 1)",
        f"datetime(2026, {next_month}, 1)"
    )

    # Replace output filename
    code = code.replace(
        "CRMLSSold202602.csv",
        f"CRMLSSold{yyyymm}.csv"
    )

    # Create temporary script
    temp_script = folder / "_temp_sold.py"

    temp_script.write_text(code)

    # Run temporary script
    subprocess.run(
        [sys.executable, str(temp_script)],
        cwd=folder,
        check=True
    )

    # Delete temporary script
    temp_script.unlink()

    print(f"FINISHED SOLD {yyyymm}")




print("\n\n##############################################")
print("STARTING LISTING DOWNLOADS")
print("##############################################")

for month, next_month, yyyymm in months:
    run_listing_month(
        month,
        next_month,
        yyyymm
    )




print("\n\n##############################################")
print("STARTING SOLD DOWNLOADS")
print("##############################################")

for month, next_month, yyyymm in months:
    run_sold_month(
        month,
        next_month,
        yyyymm
    )



print("\n\n==============================================")
print("ALL MISSING MONTHS DOWNLOADED!")
print("==============================================")

print("\nYou should now have:")

print("\nLISTINGS:")
print("CRMLSListing202605.csv")
print("CRMLSListing202606.csv")
print("CRMLSListing202607.csv")
print("CRMLSListing202608.csv")

print("\nSOLD:")
print("CRMLSSold202605.csv")
print("CRMLSSold202606.csv")
print("CRMLSSold202607.csv")
print("CRMLSSold202608.csv")
