import pandas as pd
from pathlib import Path

# Define the file paths

PARQUET_FILE = Path("data/raw/green_tripdata_2023-12.parquet") 
CSV_FILE = Path("data/raw/taxi_zone_lookup.csv")


def inspect_parquet(file_path: Path) -> None:
    """Reads a Parquet file and prints basic exploratory information."""
    print(f"--- Inspecting Parquet file: {file_path.name} ---")
    
    # Load the parquet file into a pandas DataFrame
    df = pd.read_parquet(file_path)
    
    # Print 1: Shape (Rows, Columns)
    print(f"\n1. Dimensions (Rows, Columns): {df.shape}")
    
    # Print 2: Column names
    print(f"\n2. Columns:\n{df.columns.tolist()}")
    
    # Print 3: Data types for each column
    print(f"\n3. Data types:\n{df.dtypes}")
    
    # Print 4: First 5 rows of the dataframe
    print(f"\n4. First 5 rows:")
    print(df.head())
    
    # Print 5: Count of missing (null) values per column
    print(f"\n5. Null values per column:")
    print(df.isna().sum())


def inspect_csv(file_path: Path) -> None:
    """Reads a CSV file and prints basic exploratory information."""
    print(f"\n--- Inspecting CSV file: {file_path.name} ---")
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Print 1: Shape (Rows, Columns)
    print(f"\n1. Dimensions (Rows, Columns): {df.shape}")
    
    # Print 2: First 5 rows of the dataframe
    print(f"\n2. First 5 rows:")
    print(df.head())



def inspect_quality(parquet_path: Path, zones_path: Path) -> None:
    """Performs data quality checks on the raw data."""
    trips = pd.read_parquet(parquet_path)
    zones = pd.read_csv(zones_path)

    print("\n--- Data quality checks ---")

    # Check 1: Trips outside the main month (Already provided as example)
    outside_month = (
        (trips["lpep_pickup_datetime"] < pd.Timestamp("2023-12-01"))
        | (trips["lpep_pickup_datetime"] >= pd.Timestamp("2024-01-01"))
    )
    print("1. Pickups outside December 2023:", outside_month.sum())

    # Check 2: Trips where dropoff time is before or equal to pickup time
    invalid_times = trips["lpep_dropoff_datetime"] <= trips["lpep_pickup_datetime"]
    print("2. Trips with dropoff time <= pickup time:", invalid_times.sum())

    # Check 3: Trips with zero or negative distance
    invalid_distance = trips["trip_distance"] <= 0
    print("3. Trips with non-positive distance:", invalid_distance.sum())

    # Check 4: Trips with a negative total amount
    negative_amount = trips["total_amount"] < 0
    print("4. Trips with negative total amount:", negative_amount.sum())

    # Check 5: Null values in the zone lookup LocationID
    null_zone_ids = zones["LocationID"].isna().sum()
    print("5. Null values in Zone Lookup LocationID:", null_zone_ids)

    # Check 6: Duplicated LocationIDs in the zone lookup
    dup_zone_ids = zones["LocationID"].duplicated().sum()
    print("6. Duplicated LocationIDs in Zone Lookup:", dup_zone_ids)

    # Check 7: Pickup locations not found in the zone catalog (Already provided)
    unknown_pickup = ~trips["PULocationID"].isin(zones["LocationID"])
    print("7. Trips with pickup location missing from lookup:", unknown_pickup.sum())

    # Check 8: Dropoff locations not found in the zone catalog (Your turn)
    unknown_dropoff = ~trips["DOLocationID"].isin(zones["LocationID"])
    print("8. Trips with dropoff location missing from lookup:", unknown_dropoff.sum())


    # PART 1: Combine flags and show summary

    flagged = (
        outside_month
        | invalid_times
        | invalid_distance
        | negative_amount
        | unknown_pickup
        | unknown_dropoff
    )

    print("\n--- Quality summary ---")
    print("Total trips:", len(trips))
    print("Trips with at least one flag:", flagged.sum())
    print("Trips without these flags:", (~flagged).sum())

    # This assert ensures the math is correct
    assert flagged.sum() + (~flagged).sum() == len(trips)

    # PART 2: Show examples 
    review_columns = [
        "lpep_pickup_datetime",
        "lpep_dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "trip_distance",
        "fare_amount",
        "total_amount",
        "payment_type",
    ]

    print("\n--- Pickups outside the target month ---")
    print(trips.loc[outside_month, review_columns].to_string(index=False))

    print("\n--- Sample of trips with non-positive duration ---")
    print(trips.loc[invalid_times, review_columns].head(5).to_string(index=False))

    
    print("\n--- Sample of trips with non-positive distance ---")
    print(trips.loc[invalid_distance, review_columns].head(5).to_string(index=False))

    print("\n--- Sample of trips with negative total amount ---")
    print(trips.loc[negative_amount, review_columns].head(5).to_string(index=False))


if __name__ == "__main__":
    # Check if the Parquet file exists before trying to read it
    if PARQUET_FILE.exists():
        inspect_parquet(PARQUET_FILE)
    else:
        print(f"[ERROR] File not found: {PARQUET_FILE}")
        
    # Check if the CSV file exists before trying to read it
    if CSV_FILE.exists():
        inspect_csv(CSV_FILE)
    else:
        print(f"[ERROR] File not found: {CSV_FILE}")

    # Call the data quality inspection
    if PARQUET_FILE.exists() and CSV_FILE.exists():
        inspect_quality(PARQUET_FILE, CSV_FILE)