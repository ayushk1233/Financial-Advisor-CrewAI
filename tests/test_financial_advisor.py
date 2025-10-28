import pytest
from financial_health_advisor.crew import FinancialHealthAdvisorCrew
from financial_health_advisor.tools.simple_csv_tool import simple_csv_search_tool


def test_csv_tool_basic():
    """Test that the CSV tool can read and summarize transaction data."""
    result = simple_csv_search_tool.func("data/customer_transactions.csv")
    assert "Total rows:" in result, "CSV summary should include row count"
    assert "Total amount:" in result, "CSV summary should include total amount"
    assert "Category breakdown:" in result, "CSV summary should include categories"


def test_crew_initialization():
    """Test that we can create a crew instance without errors."""
    crew = FinancialHealthAdvisorCrew()
    assert crew is not None, "Should create crew instance"
    
    crew_instance = crew.crew()
    assert crew_instance is not None, "Should create Crew object"


@pytest.mark.integration
def test_full_pipeline():
    """Integration test for the full pipeline.
    
    Note: This test requires:
    - Valid GEMINI_API_KEY in environment
    - data/customer_transactions.csv present
    - Network access for LLM calls
    
    Mark this test with @pytest.mark.integration so it can be skipped
    for quick local test runs with: pytest -m "not integration"
    """
    crew = FinancialHealthAdvisorCrew()
    result = crew.crew().kickoff()
    
    assert result is not None, "Pipeline should complete with output"
    # CrewOutput may not implement __len__; ensure string representation is non-empty
    assert str(result).strip() != "", "Pipeline should produce non-empty output"