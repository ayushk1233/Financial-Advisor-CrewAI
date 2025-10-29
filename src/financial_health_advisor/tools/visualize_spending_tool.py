import os
import matplotlib.pyplot as plt
try:
    # New CrewAI package layout
    from crewai.tools.base_tool import BaseTool
except ImportError:
    # Fallback to older package naming
    from crewai_tools import Tool as BaseTool


class VisualizeTool(BaseTool):
    name: str = "visualize_spending_tool"
    description: str = "Generates a local pie chart visualization of spending by category and saves it as a PNG file."

    def _run(self, spending_data: dict) -> str:
        """
        Create and save a spending visualization as a pie chart.

        Args:
            spending_data (dict): e.g. {"Rent": 1200, "Groceries": 400, "Utilities": 150}

        Returns:
            str: Markdown-compatible image link to embed in the report.
        """
        try:
            if not spending_data or not isinstance(spending_data, dict):
                return "⚠️ No valid spending data to visualize."

            labels = list(spending_data.keys())
            values = [abs(v) for v in spending_data.values()]

            # Create chart
            plt.figure(figsize=(6, 6))
            plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            plt.title("Monthly Spending Breakdown")

            # Ensure output directory exists
            os.makedirs("data", exist_ok=True)
            chart_path = "data/spending_chart.png"

            plt.savefig(chart_path, bbox_inches="tight")
            plt.close()

            # Return Markdown link for embedding
            return f"![Monthly Spending Breakdown]({chart_path})"

        except Exception as e:
            return f"⚠️ Visualization error: {e}"


# Register tool instance for CrewAI
visualize_spending_tool = VisualizeTool()