import json
import datetime

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self.load_expenses()
        self.user_id = None

    def load_expenses(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_expenses(self):
        with open(self.filename, "w") as file:
            json.dump(self.expenses, file, indent=4)

    def login(self, user_id):
        self.user_id = user_id
        if user_id not in self.expenses:
            self.expenses[user_id] = []
        print(f"Logged in as: {user_id}")
        
    def add_expense(self, amount, category, description):
        if not self.user_id:
            print("Please log in first.")
            return
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.expenses[self.user_id].append(expense)
        self.save_expenses()
        print("Expense added successfully.")

    def list_expenses(self):
        if not self.user_id:
            print("Please log in first.")
            return
        if not self.expenses[self.user_id]:
            print("No expenses recorded.")
            return
        for idx, expense in enumerate(self.expenses[self.user_id], 1):
            print(f"{idx}. {expense['date']} - {expense['category']} - ${expense['amount']} - {expense['description']}")

    def total_expense(self):
        if not self.user_id:
            print("Please log in first.")
            return
        total = sum(expense["amount"] for expense in self.expenses[self.user_id])
        print(f"Total expenses: ${total}")

    def filter_by_category(self, category):
        if not self.user_id:
            print("Please log in first.")
            return
        filtered = [e for e in self.expenses[self.user_id] if e["category"].lower() == category.lower()]
        if not filtered:
            print(f"No expenses found in category: {category}")
            return
        for idx, expense in enumerate(filtered, 1):
            print(f"{idx}. {expense['date']} - ${expense['amount']} - {expense['description']}")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    while True:
        print("\nExpense Tracker")
        print("1. Log In")
        print("2. Add Expense")
        print("3. List Expenses")
        print("4. Show Total Expense")
        print("5. Filter by Category")
        print("6. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            user_id = input("Enter your user ID: ")
            tracker.login(user_id)
        elif choice == "2":
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(amount, category, description)
        elif choice == "3":
            tracker.list_expenses()
        elif choice == "4":
            tracker.total_expense()
        elif choice == "5":
            category = input("Enter category to filter: ")
            tracker.filter_by_category(category)
        elif choice == "6":
            print("Exiting Expense Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")
