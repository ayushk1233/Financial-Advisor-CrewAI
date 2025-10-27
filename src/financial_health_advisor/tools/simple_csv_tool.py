import pandas as pd
from typing import Optional
from crewai.tools import tool


@tool("Simple CSV Search Tool")
def simple_csv_search_tool(file_path: Optional[str] = None) -> str:
    """Read and summarize CSV transaction data (totals and category breakdown).

    This function is decorated with `@tool` so it returns a CrewAI-compatible tool
    object that the Agent can accept directly in its `tools` list.
    """
    if not file_path:
        file_path = "data/customer_transactions.csv"

    try:
        df = pd.read_csv(file_path)

        summary = []
        summary.append(f"Total rows: {len(df)}")
        summary.append(f"Columns: {', '.join(df.columns)}")

        if 'Amount' in df.columns:
            total_amount = df['Amount'].sum()
            summary.append(f"Total amount: ${total_amount:,.2f}")

        if 'Category' in df.columns and 'Amount' in df.columns:
            category_summary = df.groupby('Category')['Amount'].sum().to_dict()
            summary.append("\nCategory breakdown:")
            for category, amount in category_summary.items():
                summary.append(f"- {category}: ${amount:,.2f}")

        return "\n".join(summary)

    except Exception as e:
        return f"Error analyzing CSV data: {e}"