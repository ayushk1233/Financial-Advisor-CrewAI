"""Test configuration and fixtures for the financial_health_advisor tests."""
import os
import sys
import pytest
from pathlib import Path

# Add src directory to Python path for test runs
SRC_DIR = Path(__file__).parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Test data paths
TEST_DATA_DIR = Path(__file__).parent.parent / "data"

@pytest.fixture
def test_csv_path():
    """Return path to test CSV file."""
    return str(TEST_DATA_DIR / "customer_transactions.csv")

@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("GEMINI_API_KEY", "test_key")
    monkeypatch.setenv("GEMINI_MODEL", "models/gemini-pro-latest")
    monkeypatch.setenv("SERPER_API_KEY", "test_serper_key")
    monkeypatch.setenv("LOG_LEVEL", "INFO")