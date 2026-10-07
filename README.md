# ETL Pipeline with Python and Pytest

This project implements an ETL pipeline using Python.

The pipeline extracts data from a REST API, transforms the data using Pandas, and loads the processed data into a CSV file.

Pytest is used to perform unit testing of the ETL functions.

## Technologies

- Python
- Pandas
- Requests
- Pytest
- REST API
- CSV

## ETL Flow

REST API -> Extract -> Transform using Pandas -> Load -> CSV -> Pytest Unit Tests

## API

https://jsonplaceholder.typicode.com/posts

## Installation

python -m venv venv

Windows:

venv\Scripts\activate

pip install -r requirements.txt

## Run

python main.py

## Test

pytest

## Project Structure

src/etl.py contains the ETL functions.

main.py executes the pipeline.

tests/test_etl.py contains pytest unit tests.

data/posts.csv contains the processed output.
