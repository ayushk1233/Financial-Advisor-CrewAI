#!/usr/bin/env python
import os
from dotenv import load_dotenv
from crew import FinancialHealthAdvisorCrew

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