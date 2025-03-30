import sys
from collections import defaultdict

def load_transactions(filename):
    transactions = defaultdict(list)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    account, date, amount = parts
                    transactions[account].append((date, int(amount)))
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)
    return transactions

def show_total_expenses(transactions, account):
    total = sum(amount for _, amount in transactions.get(account, []))
    print(f"Total expenses for {account}: {total}")

def show_all_transactions(transactions, account):
    print(f"Transactions for {account}:")
    for date, amount in sorted(transactions.get(account, [])):
        print(f"{date}: {amount}")

def show_expenses_on_date(transactions, account, date):
    total = sum(amount for d, amount in transactions.get(account, []) if d == date)
    print(f"Total expenses on {date} for {account}: {total}")

def show_daily_average_expenses(transactions, account, year_month):
    daily_expenses = defaultdict(int)
    days = set()
    for date, amount in transactions.get(account, []):
        if date.startswith(year_month):
            daily_expenses[date] += amount
            days.add(date)
    avg = sum(daily_expenses.values()) / len(days) if days else 0
    print(f"Daily average expenses in {year_month} for {account}: {avg:.2f}")

def main():
    transactions = load_transactions("input.txt")
    while True:
        print("\n1. Show total expenses")
        print("2. Show all transactions")
        print("3. Show expenses on a specific day")
        print("4. Show daily average expenses on a specific month")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == '5':
            print("Exiting...")
            break
        
        account = input("Enter account number: ")
        if choice == '1':
            show_total_expenses(transactions, account)
        elif choice == '2':
            show_all_transactions(transactions, account)
        elif choice == '3':
            date = input("Enter date (YYYYMMDD): ")
            show_expenses_on_date(transactions, account, date)
        elif choice == '4':
            year_month = input("Enter year and month (YYYYMM): ")
            show_daily_average_expenses(transactions, account, year_month)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
