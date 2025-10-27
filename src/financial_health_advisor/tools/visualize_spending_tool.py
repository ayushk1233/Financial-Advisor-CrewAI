from crewai.tools import tool
import pandas as pd
import matplotlib.pyplot as plt


@tool("Visualize Spending Tool")
def visualize_spending_tool(csv_path: str) -> str:
    """
    Creates a pie chart visualization of spending by category from CSV data.
    Input should be the path to a CSV file with 'Category', 'Amount', and 'Type' columns.
    """
    try:
        df = pd.read_csv(csv_path)
        
        # Filter spending transactions (Expense type)
        spending = df[df['Type'] == 'Expense'].copy()
        
        # Group by category
        category_spending = spending.groupby('Category')['Amount'].sum()
        
        # Create pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(category_spending.values, labels=category_spending.index, autopct='%1.1f%%')
        plt.title('Spending Breakdown by Category')
        plt.savefig('spending_breakdown.png')
        plt.close()
        
        return "Spending visualization saved as 'spending_breakdown.png'"
    
    except Exception as e:
        return f"Error creating visualization: {str(e)}"