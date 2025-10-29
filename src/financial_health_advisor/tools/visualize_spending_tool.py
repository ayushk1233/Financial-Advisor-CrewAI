import os
import matplotlib.pyplot as plt
from typing import Dict
from crewai.tools import BaseTool


class VisualizeTool(BaseTool):
    name: str = "Visualize Spending Tool"
    description: str = "Generates a pie chart visualization of spending data and saves it locally."

    def _run(self, spending_data: Dict[str, float]) -> str:
        """
        Generates a pie chart visualization of spending data and saves it locally.

        Args:
            spending_data (Dict[str, float]): Category-to-amount mapping, e.g.,
                {"Rent": 1200, "Groceries": 400, "Utilities": 150}

        Returns:
            str: Markdown image link to embed the local pie chart.
        """
        try:
            # Validate input
            if not spending_data or not isinstance(spending_data, dict):
                return "⚠️ No valid spending data available for visualization."

            # Ensure categories and values
            labels = list(spending_data.keys())
            values = list(spending_data.values())

            if len(labels) == 0 or sum(values) == 0:
                return "⚠️ Spending data is empty or sums to zero."

            # Sort by value descending for consistent charts
            items = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
            labels, values = zip(*items)

            # Create chart
            plt.figure(figsize=(6, 6))
            # Use a readable colormap
            cmap = plt.get_cmap('tab20')
            colors = [cmap(i % 20) for i in range(len(labels))]

            wedges, texts, autotexts = plt.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors,
                textprops={'fontsize': 10}
            )

            plt.title("Monthly Spending by Category", fontsize=14)
            # Improve contrast for autotexts
            for t in autotexts:
                t.set_color('white')

            # Save chart in project root's data directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            data_dir = os.path.join(project_root, "data")
            os.makedirs(data_dir, exist_ok=True)
            
            chart_path = os.path.join(data_dir, "spending_chart.png")
            plt.savefig(chart_path, bbox_inches="tight", dpi=300)
            plt.close()
            
            print(f"Chart saved to: {chart_path}")
            # Return markdown image path (relative to project root)
            return f"![Spending Distribution](data/spending_chart.png)"

        except Exception as e:
            # Return a friendly error message; do not raise to avoid crashing the report generation
            return f"⚠️ Visualization error: {e}"


# Create an instance of the tool
visualize_spending_tool = VisualizeTool()