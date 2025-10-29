import os
import pandas as pd
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from financial_health_advisor.tools.visualize_spending_tool import visualize_spending_tool
from financial_health_advisor.tools.simple_csv_tool import simple_csv_search_tool
from financial_health_advisor.llm.gemini_llm import GeminiLLM
from google.api_core.exceptions import GoogleAPIError
def read_csv_summary(file_path: str = "data/customer_transactions.csv") -> str:
    """Read and summarize CSV data"""
    try:
        df = pd.read_csv(file_path)
        summary = []
        summary.append(f"Total rows: {len(df)}")
        if 'Amount' in df.columns:
            total_amount = df['Amount'].sum()
            summary.append(f"Total amount: ${total_amount:,.2f}")
        if 'Category' in df.columns:
            category_summary = df.groupby('Category')['Amount'].sum().to_dict()
            summary.append("\nCategory breakdown:")
            for category, amount in category_summary.items():
                summary.append(f"- {category}: ${amount:,.2f}")
        return "\n".join(summary)
    except Exception as e:
        return f"Error reading CSV: {str(e)}"

def safe_gemini_llm():
    # If no API key is present, avoid making network calls and return None.
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("⚠️ GEMINI_API_KEY not set; Gemini LLM will not be initialized.")
        return None

    try:
        llm = GeminiLLM()
        # Optionally test the LLM with a simple prompt to verify it works.
        # Wrap in try/except to avoid crashing if the network or credentials fail.
        try:
            test_response = llm.call("Test connection.")
            if not test_response or str(test_response).lower().startswith('error'):
                raise GoogleAPIError("Empty or error response from Gemini")
        except Exception:
            print("⚠️ Warning: Gemini test call failed — continuing with LLM object (calls may fail at runtime).")
        return llm
    except Exception as e:
        print(f"⚠️ Gemini initialization error: {e}")
        return None

# Initialize our custom Gemini LLM with model from environment and safety checks
model_name = os.getenv('GEMINI_MODEL', 'models/gemini-pro-latest')
print(f"🔧 Initializing Gemini with model: {model_name}")
gemini_llm = safe_gemini_llm()

# Initialize tools
csv_tool = simple_csv_search_tool


@CrewBase
class FinancialHealthAdvisorCrew():
    """Financial Health Advisor Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def data_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['data_reader'],
            tools=[csv_tool, visualize_spending_tool],  # CSV tool and visualization tool
            llm=gemini_llm,  # Using Gemini LLM explicitly
            verbose=True,
            memory=True
        )

    @agent
    def advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['advisor'],
            tools=[SerperDevTool()],
            llm=gemini_llm,  # Using Gemini LLM explicitly
            verbose=True
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'],
            llm=gemini_llm,  # Using Gemini LLM explicitly
            verbose=True
        )

    @task
    def read_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['read_data_task'],
        )

    @task
    def advise_task(self) -> Task:
        return Task(
            config=self.tasks_config['advise_task'],
        )

    def embed_spending_visual(self):
        try:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data/customer_transactions.csv")
            print(f"Reading CSV from: {csv_path}")
            df = pd.read_csv(csv_path)
            print("CSV data loaded")
            
            # Get expenses and convert amounts to positive values
            print("Filtering and processing expenses...")
            df['Amount'] = df['Amount'].abs()  # Convert all amounts to positive
            expense_data = df[df["Type"].str.strip().str.lower() == "expense"]
            
            if expense_data.empty:
                print("⚠️ No expense data found")
                return "⚠️ No expense data found in the transactions."
            
            print(f"Found {len(expense_data)} expense records")
            # Group by category and sum the (now positive) amounts
            category_data = expense_data.groupby("Category")["Amount"].sum().to_dict()
            print(f"Category data: {category_data}")
            
            # Access and call the visualization tool using run()
            image_markdown = visualize_spending_tool.run(category_data)
            print(f"Generated markdown: {image_markdown}")
            return image_markdown
        except Exception as e:
            print(f"❌ Error in embed_spending_visual: {str(e)}")
            return f"⚠️ Visualization could not be generated: {str(e)}"

    @task
    def write_report_task(self) -> Task:
        visualization_md = self.embed_spending_visual()
        # Use the current working directory (which is set to project root in main.py)
        report_path = os.path.abspath('financial_health_report.md')
        
        return Task(
            config=self.tasks_config['write_report_task'],
            output_file=report_path,
            additional_context=f"\n\n### Spending Visualization\n{visualization_md}\n"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Financial Health Advisor crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )