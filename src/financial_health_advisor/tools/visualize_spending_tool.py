import os
import matplotlib.pyplot as plt
from crewai.tools import tool


@tool
def visualize_spending_tool(spending_data: dict) -> str:
    """
    Generates a pie chart visualization of spending data and saves it locally.

    Args:
        spending_data (dict): Category-to-amount mapping, e.g.,
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

        # Save chart locally
        os.makedirs("data", exist_ok=True)
        chart_path = os.path.join("data", "spending_chart.png")
        plt.savefig(chart_path, bbox_inches="tight", dpi=300)
        plt.close()

        # Return markdown image path (relative)
        return f"![Spending Distribution](data/spending_chart.png)"

    except Exception as e:
        # Return a friendly error message; do not raise to avoid crashing the report generation
        return f"⚠️ Visualization error: {e}"
