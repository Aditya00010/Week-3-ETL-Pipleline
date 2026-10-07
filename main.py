from pathlib import Path
from src.etl import run_pipeline


API_URL = "https://jsonplaceholder.typicode.com/posts"
OUTPUT_FILE = Path("data/posts.csv")


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df = run_pipeline(API_URL, OUTPUT_FILE)

    print("ETL Pipeline completed successfully")
    print(f"Records processed: {len(df)}")
    print(f"CSV file created: {OUTPUT_FILE}")
    print(df.head())


if __name__ == "__main__":
    main()
