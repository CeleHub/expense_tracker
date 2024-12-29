import pandas as pd
import matplotlib.pyplot as plt
import os
from colorama import Fore, Style, init

# Initialize colorama for colored text
init(autoreset=True)

# File to store transactions
FILE_NAME = "transactions.csv"

def print_header(title):
    """Display a styled header."""
    print(Fore.CYAN + "\n" + "=" * 40)
    print(f"{title:^40}")
    print("=" * 40 + Style.RESET_ALL)

def main_menu():
    """Display the main menu."""
    print_header("Personal Expense Tracker")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Analyze Expenses")
    print("4. Export/Import Data")
    print("5. Exit")
    choice = input(Fore.YELLOW + "Choose an option (1-5): ").strip()
    return choice

def add_transaction():
    """Add a new transaction."""
    print_header("Add a Transaction")
    try:
        amount = float(input("Enter amount (e.g., 100.50): "))
        t_type = input("Type (Income/Expense): ").capitalize()
        if t_type not in ["Income", "Expense"]:
            print(Fore.RED + "Invalid type! Please enter 'Income' or 'Expense'.")
            return
        category = input("Category (e.g., Food, Rent, Salary): ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()

        # Save to file or list
        transaction = {"Amount": amount, "Type": t_type, "Category": category, "Date": date}
        save_transaction(transaction)
        print(Fore.GREEN + "Transaction added successfully!")
    except ValueError:
        print(Fore.RED + "Invalid amount! Please enter a valid number.")

def save_transaction(transaction):
    """Save a transaction to the CSV file."""
    df = pd.DataFrame([transaction])
    if not os.path.exists(FILE_NAME):
        df.to_csv(FILE_NAME, index=False)
    else:
        df.to_csv(FILE_NAME, mode='a', header=False, index=False)

def view_transactions():
    """Display all transactions in a tabular format."""
    print_header("View Transactions")
    if not os.path.exists(FILE_NAME):
        print(Fore.RED + "No transactions found. Start adding some!")
        return

    # Read data from the CSV file
    df = pd.read_csv(FILE_NAME)
    print(Fore.GREEN + df.to_string(index=False))  # Display in tabular format

    # Optional: Allow the user to filter by type or category
    filter_option = input("\nFilter by (Type/Category/None): ").capitalize()
    if filter_option == "Type":
        t_type = input("Enter type (Income/Expense): ").capitalize()
        filtered_df = df[df['Type'] == t_type]
        print(Fore.BLUE + filtered_df.to_string(index=False))
    elif filter_option == "Category":
        category = input("Enter category: ").strip()
        filtered_df = df[df['Category'] == category]
        print(Fore.BLUE + filtered_df.to_string(index=False))
    else:
        print(Fore.YELLOW + "Returning to the main menu.")

def analyze_expenses():
    """Analyze total income, expenses, and visualize data."""
    print_header("Analyze Expenses")
    if not os.path.exists(FILE_NAME):
        print(Fore.RED + "No transactions found. Start adding some!")
        return

    # Read data from the CSV file
    df = pd.read_csv(FILE_NAME)

    # Calculate totals
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expenses = df[df['Type'] == 'Expense']['Amount'].sum()
    print(Fore.GREEN + f"Total Income: ${total_income:.2f}")
    print(Fore.RED + f"Total Expenses: ${total_expenses:.2f}")

    # Visualization: Pie chart for categories
    expense_data = df[df['Type'] == 'Expense']
    if not expense_data.empty:
        category_sums = expense_data.groupby('Category')['Amount'].sum()
        category_sums.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title("Expenses by Category")
        plt.ylabel("")  # Remove the y-axis label for better visualization
        plt.show()
    else:
        print(Fore.YELLOW + "No expenses to visualize.")

def export_data():
    """Export all transactions to a user-specified file."""
    print_header("Export Data")
    if not os.path.exists(FILE_NAME):
        print(Fore.RED + "No transactions to export. Start adding some!")
        return

    # Ask the user for the export file name
    export_file = input("Enter the export file name (e.g., backup.csv): ").strip()
    try:
        # Copy the existing file to the new location
        df = pd.read_csv(FILE_NAME)
        df.to_csv(export_file, index=False)
        print(Fore.GREEN + f"Transactions successfully exported to '{export_file}'.")
    except Exception as e:
        print(Fore.RED + f"Error exporting data: {e}")

def import_data():
    """Import transactions from a user-specified file."""
    print_header("Import Data")
    import_file = input("Enter the file name to import (e.g., backup.csv): ").strip()
    if not os.path.exists(import_file):
        print(Fore.RED + f"File '{import_file}' not found.")
        return

    try:
        # Read the import file and append data to the existing file
        imported_df = pd.read_csv(import_file)
        if not os.path.exists(FILE_NAME):
            imported_df.to_csv(FILE_NAME, index=False)
        else:
            imported_df.to_csv(FILE_NAME, mode='a', header=False, index=False)

        print(Fore.GREEN + f"Transactions successfully imported from '{import_file}'.")
    except Exception as e:
        print(Fore.RED + f"Error importing data: {e}")

def main():
    """Main program loop."""
    while True:
        choice = main_menu()
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            analyze_expenses()
        elif choice == "4":
            print_header("Export/Import Options")
            print("1. Export Data")
            print("2. Import Data")
            sub_choice = input(Fore.YELLOW + "Choose an option (1-2): ").strip()
            if sub_choice == "1":
                export_data()
            elif sub_choice == "2":
                import_data()
            else:
                print(Fore.RED + "Invalid option.")
        elif choice == "5":
            print(Fore.CYAN + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()
