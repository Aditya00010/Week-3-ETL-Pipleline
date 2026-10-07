import pandas as pd
import pytest
from unittest.mock import Mock
import src.etl as etl


def test_extract_data(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "userId": 1,
            "id": 1,
            "title": "test title",
            "body": "test body"
        }
    ]
    mock_response.raise_for_status.return_value = None

    def mock_get(url, timeout):
        return mock_response

    monkeypatch.setattr(etl.requests, "get", mock_get)

    result = etl.extract_data("https://example.com/api")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_extract_data_failure(monkeypatch):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = etl.requests.RequestException(
        "API Error"
    )

    def mock_get(url, timeout):
        return mock_response

    monkeypatch.setattr(etl.requests, "get", mock_get)

    with pytest.raises(etl.requests.RequestException):
        etl.extract_data("https://example.com/api")


def test_transform_data():
    data = [
        {
            "userId": 1,
            "id": 1,
            "title": "  hello world  ",
            "body": "  sample body  "
        }
    ]

    result = etl.transform_data(data)

    assert isinstance(result, pd.DataFrame)
    assert result.iloc[0]["title"] == "Hello World"
    assert result.iloc[0]["body"] == "sample body"


def test_transform_empty_data():
    result = etl.transform_data([])

    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_transform_duplicate_data():
    data = [
        {
            "userId": 1,
            "id": 1,
            "title": "hello",
            "body": "body"
        },
        {
            "userId": 1,
            "id": 1,
            "title": "hello",
            "body": "body"
        }
    ]

    result = etl.transform_data(data)

    assert len(result) == 1


def test_load_data(tmp_path):
    data = {
        "id": [1, 2],
        "title": ["First", "Second"]
    }

    df = pd.DataFrame(data)
    output_file = tmp_path / "output.csv"

    result = etl.load_data(df, output_file)

    assert result == output_file
    assert output_file.exists()

    loaded_df = pd.read_csv(output_file)

    assert len(loaded_df) == 2
    assert list(loaded_df.columns) == ["id", "title"]


def test_run_pipeline(monkeypatch, tmp_path):
    data = [
        {
            "userId": 1,
            "id": 1,
            "title": "test title",
            "body": "test body"
        }
    ]

    monkeypatch.setattr(etl, "extract_data", lambda url: data)

    output_file = tmp_path / "posts.csv"

    result = etl.run_pipeline(
        "https://example.com/api",
        output_file
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert output_file.exists()
