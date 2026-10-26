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