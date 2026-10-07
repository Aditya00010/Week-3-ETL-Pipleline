import requests
import pandas as pd


def extract_data(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def transform_data(data):
    df = pd.DataFrame(data)

    if df.empty:
        return df

    df = df.drop_duplicates()

    if "title" in df.columns:
        df["title"] = df["title"].astype(str).str.strip().str.title()

    if "body" in df.columns:
        df["body"] = df["body"].astype(str).str.strip()

    if "userId" in df.columns:
        df["userId"] = pd.to_numeric(df["userId"], errors="coerce").astype("Int64")

    return df


def load_data(df, output_file):
    df.to_csv(output_file, index=False)
    return output_file


def run_pipeline(url, output_file):
    data = extract_data(url)
    df = transform_data(data)
    load_data(df, output_file)
    return df
