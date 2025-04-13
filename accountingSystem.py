import sys
from collections import defaultdict
from datetime import datetime

def load_transactions(filename):
    """
    Reads transaction data from a file line by line.
    Each line should have: account date amount (e.g., "userA 20230101 100").
    If the file is missing, the program prints an error and exits.
    Returns a dictionary with account IDs as keys and a list of (date, amount) pairs.
    """
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
    """
    Calculates and prints the total amount spent by a specific account.
    It simply sums all the amounts linked to the given account ID.
    """
    total = sum(amount for _, amount in transactions.get(account, []))
    print(f"Total expenses for {account}: {total}")

def show_all_transactions(transactions, account):
    """
    Lists out every transaction tied to the given account.
    Transactions are shown in ascending date order.
    """
    print(f"Transactions for {account}:")
    for date, amount in sorted(transactions.get(account, [])):
        print(f"{date}: {amount}")

def show_expenses_on_date(transactions, account, date):
    """
    Displays how much was spent on a specific date (YYYYMMDD).
    If the date format is off or invalid, it prints an error message.
    """
    if len(date) != 8 or not date.isdigit():
        print("Invalid date format. Use YYYYMMDD.")
        return
    try:
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        print("Invalid date (e.g. month/day out of range). Use YYYYMMDD.")
        return

    total = sum(amount for d, amount in transactions.get(account, []) if d == date)
    print(f"Total expenses on {date} for {account}: {total}")

def show_daily_average_expenses(transactions, account, year_month):
    """
    Shows the average daily expenses for a particular month (YYYYMM).
    If the format is incorrect or invalid, it prints a warning and exits early.
    """
    if len(year_month) != 6 or not year_month.isdigit():
        print("Invalid month format. Use YYYYMM.")
        return
    try:
        datetime.strptime(year_month + "01", "%Y%m%d")
    except ValueError:
        print("Invalid month (e.g. month out of range). Use YYYYMM.")
        return

    daily_expenses = defaultdict(int)
    days = set()
    for date, amount in transactions.get(account, []):
        if date.startswith(year_month):
            daily_expenses[date] += amount
            days.add(date)
    avg = sum(daily_expenses.values()) / len(days) if days else 0
    print(f"Daily average expenses in {year_month} for {account}: {avg:.2f}")

def main():
    """
    Main function that:
      - Loads data from "input.txt"
      - Asks for an account ID, or Q to quit
      - Displays a menu for expenses queries
      - Loops until the user chooses to exit
    """
    transactions = load_transactions("input.txt")
    while True:
        account = input("Enter ID or Q to quit: ")
        if account.upper() == 'Q':
            print("Exiting...")
            break
        elif account not in transactions:
            print("Invalid ID. Try again.")
            continue

        print(f"Welcome {account}")
        while True:
            print("\nEnter command:")
            print("1) A Show total expenses")
            print("2) B Show all transactions")
            print("3) C Show expenses on a specific day")
            print("4) D Show daily average expenses on a specific month")
            print("5) Q Exit system")

            choice = input("Enter choice: ").upper()
            if choice == 'Q':
                break
            elif choice == 'A':
                show_total_expenses(transactions, account)
            elif choice == 'B':
                show_all_transactions(transactions, account)
            elif choice == 'C':
                date = input("Enter date (YYYYMMDD): ")
                show_expenses_on_date(transactions, account, date)
            elif choice == 'D':
                year_month = input("Enter year and month (YYYYMM): ")
                show_daily_average_expenses(transactions, account, year_month)
            else:
                print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
