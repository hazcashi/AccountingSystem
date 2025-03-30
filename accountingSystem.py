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
    if not date.isdigit() or len(date) != 8:
        print("Invalid date format. Use YYYYMMDD.")
        return
    total = sum(amount for d, amount in transactions.get(account, []) if d == date)
    print(f"Total expenses on {date} for {account}: {total}")

def show_daily_average_expenses(transactions, account, year_month):
    if not year_month.isdigit() or len(year_month) != 6:
        print("Invalid month format. Use YYYYMM.")
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
