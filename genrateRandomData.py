import random
from datetime import datetime, timedelta
import csv

def generate_random_data(num_entries):
    categories = ["Income", "Expense"]
    income_descriptions = ["Salary", "Freelance Work", "Side Gig", "Investments"]
    expense_descriptions = ["Groceries", "Rent", "Utilities", "Entertainment", "Travel", "Shopping"]
    start_date = datetime.now()

    data = []
    for _ in range(num_entries):
        date = (start_date - timedelta(days=random.randint(0, 365))).strftime("%d-%m-%Y")
        amount = round(random.uniform(50.0, 1000.0), 2)
        category = random.choice(categories)
        if category == "Income":
            description = random.choice(income_descriptions)
        else:
            description = random.choice(expense_descriptions)

        data.append({'date': date, 'amount': amount, 'category': category, 'description': description})

    # Trier les données par date
    data.sort(key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y"))

    with open('finance_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'amount', 'category', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Generate 50 random entries
generate_random_data(50)