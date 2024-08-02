import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_amount, get_category, get_date, get_description

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"
    
    @classmethod
    def initialize_csv(self):
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.CSV_FILE, index=False)
            
    @classmethod
    def add_entry(self, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        
        with open(self.CSV_FILE, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")
        
    @classmethod
    def get_transactions(self, start_date: str, end_date: str) -> pd.DataFrame | None:
        df = pd.read_csv(self.CSV_FILE)
        
        df["date"] = pd.to_datetime(df["date"], format=self.FORMAT)
        
        start_date = datetime.strptime(start_date, self.FORMAT)
        end_date = datetime.strptime(end_date, self.FORMAT)
        
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            print("No transaction found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(self.FORMAT)} to {end_date.strftime(self.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(self.FORMAT)}
                )
            )
            
            mask_income = filtered_df["category"] == "Income"
            mask_expense = filtered_df["category"] == "Expense"
        
            total_income = filtered_df[mask_income]["amount"].sum()
            total_expense = filtered_df[mask_expense]["amount"].sum()
            
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
            return filtered_df
        
def add():
    CSV.initialize_csv()
    
    date = get_date("Enter the date of the transaction (dd-mm-yyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    
    CSV.add_entry(date=date, amount=amount, category=category, description=description)
     
def plot_transactions(df: pd.DataFrame):
    df.set_index("date", inplace=True)
    
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
     
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Inome and Expense over time")
    plt.legend()
    plt.grid(True)
    plt.show()
         
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transaction and summary within a date range")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ") 
            end_date = get_date("Enter the end date (dd-mm-yyyy): ") 
            
            df = CSV.get_transactions(start_date, end_date)
            
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")
            
if __name__ == "__main__":
    main()