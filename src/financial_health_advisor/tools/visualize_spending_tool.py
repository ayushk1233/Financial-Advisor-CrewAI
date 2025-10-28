import os
import matplotlib.pyplot as plt
from crewai.tools import tool

@tool("visualize_spending_tool")
def visualize_spending_tool(spending_data: dict) -> str:
    """
    Create and save a pie chart of spending by category.
    Args:
        spending_data (dict): Example - {"Rent": 1200, "Groceries": 400}
    Returns:
        str: Markdown link to the saved image for embedding in reports.
    """
    try:
        labels = list(spending_data.keys())
        values = list(spending_data.values())
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("Spending Distribution by Category")
        plt.tight_layout()

        os.makedirs("data", exist_ok=True)
        chart_path = os.path.join("data", "spending_chart.png")
        plt.savefig(chart_path)
        plt.close()

        return f"![Spending Distribution]({chart_path})"
    except Exception as e:
        return f"Error generating visualization: {str(e)}"
