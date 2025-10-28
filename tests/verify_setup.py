"""Quick verification script for the Financial Health Advisor."""
import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Run basic verification of imports and functionality."""
    print("🔍 Testing imports...")
    
    # Test CSV tool
    print("\nTesting CSV tool...")
    from financial_health_advisor.tools.simple_csv_tool import simple_csv_search_tool
    result = simple_csv_search_tool.func("data/customer_transactions.csv")
    print(result[:200] + "...")
    
    # Test visualization tool
    print("\nTesting visualization tool...")
    from financial_health_advisor.tools.visualize_spending_tool import visualize_spending_tool
    test_data = {"Rent": 1200, "Groceries": 400, "Utilities": 200}
    viz_result = visualize_spending_tool.func(test_data)
    print(f"Visualization result: {viz_result}")
    
    # Test crew creation
    print("\nTesting crew creation...")
    from financial_health_advisor.crew import FinancialHealthAdvisorCrew
    crew = FinancialHealthAdvisorCrew()
    print("✅ Crew created successfully")
    
    # Test agent setup
    print("\nTesting agent initialization...")
    data_reader = crew.data_reader()
    advisor = crew.advisor()
    report_writer = crew.report_writer()
    print("✅ All agents initialized")
    
    return True

if __name__ == "__main__":
    success = main()
    print("\n✨ All tests completed successfully!" if success else "\n❌ Tests failed!")