# NYC Taxi Pipeline

Batch data pipeline that ingests, transforms, and loads NYC Green Taxi trip data and Taxi Zone Lookup data into a PostgreSQL database.

## Architecture (WIP)
- **Extract:** Reads `.parquet` and `.csv` files from `data/raw/`.
- **Transform:** Cleans, validates, and joins the data using pandas.
- **Load:** Loads the processed data into PostgreSQL running on Docker.

## Tech Stack
- Python (pandas, pyarrow)
- PostgreSQL
- Docker & Docker Compose
- pytest (upcoming)

## How to run
1. Create virtual environment: `python -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Place raw data in `data/raw/` (ignored by Git)
5. Run inspection: `python inspect_data.py`