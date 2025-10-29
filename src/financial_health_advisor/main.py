#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Get the project root directory (where main.py is located)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add src to Python path
SRC_ROOT = os.path.join(PROJECT_ROOT, 'src')
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

# Change working directory to project root
os.chdir(PROJECT_ROOT)

from financial_health_advisor.crew import FinancialHealthAdvisorCrew

# Load environment variables
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


def run():
    """
    Run the Financial Health Advisor crew using Gemini LLM.
    """
    print("🤖 Starting Financial Health Advisor with Google Gemini LLM...")
    inputs = {
        'csv_path': os.path.join(PROJECT_ROOT, 'data/customer_transactions.csv')
    }
    
    FinancialHealthAdvisorCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()