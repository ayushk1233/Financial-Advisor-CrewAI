import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_synthetic_financial_data(
    output_dir="data",
    file_name="customer_transactions.csv",
    num_records=100
):
    # Define realistic categories and mapping to income/expense
    categories = [
        "Salary", "Freelance Work", "Rent", "Groceries", "Utilities",
        "Loan Repayment", "Entertainment", "Investment", "Medical",
        "Travel", "Insurance", "Savings", "Dining Out", "Internet Bill"
    ]
    
    type_mapping = {
        "Salary": "Income",
        "Freelance Work": "Income",
        "Investment": "Income",
        "Savings": "Expense",
        "Insurance": "Expense",
        "Loan Repayment": "Expense",
        "Rent": "Expense",
        "Groceries": "Expense",
        "Utilities": "Expense",
        "Entertainment": "Expense",
        "Medical": "Expense",
        "Travel": "Expense",
        "Dining Out": "Expense",
        "Internet Bill": "Expense"
    }
    
    # Randomized start date and records
    start_date = datetime(2025, 1, 1)
    data = []
    
    for _ in range(num_records):
        # Randomize date within 90 days from start
        date = start_date + timedelta(days=random.randint(0, 90))
        category = random.choice(categories)
        t_type = type_mapping[category]
        
        # Set amount range based on type
        if t_type == "Income":
            amount = random.randint(2000, 8000)
        else:
            amount = random.randint(50, 2000)
        
        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
            "Type": t_type
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(output_dir, file_name)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Synthetic financial data created: {output_path}")
    print(df.head())

# Run generator
if __name__ == "__main__":
    generate_synthetic_financial_data(num_records=100)