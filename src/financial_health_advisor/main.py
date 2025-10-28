#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Ensure `src` is on sys.path so package imports work when running this script
ROOT = os.path.dirname(os.path.dirname(__file__))  # src/
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

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
        'csv_path': 'data/customer_transactions.csv'
    }
    
    FinancialHealthAdvisorCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()