from gui import *
from PyQt6.QtWidgets import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.submitincome_button.clicked.connect(self.submit_income)
        self.expensesubmit_button.clicked.connect(self.submit_expense)
        self.get_budget_amount()

    def get_budget_amount(self) -> None:
        """
        This function gets the current total budget amount
        This is used on initializing the GUI to grab the most up-to-date amount for the balance_label widget to display
        """
        budget_amount = 0.0
        with open("budgetdata.csv", "r", newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            for line in csvreader:
                try:
                    budget_amount = float(line[-1])
                except ValueError:
                    budget_amount = 0.0

        self.balance_label.setText(f"${budget_amount:.2f}")

    def submit_income(self) -> None:
        """
        This function defines what is to occur when pressing the submit button on the income tab
        """
        try:
            if self.hourlywage_entry.text() and self.hoursworked_entry.text():
                wage_calculation = float(self.hourlywage_entry.text()) * float(self.hoursworked_entry.text())
                current_total = 0.0
                with open("budgetdata.csv", "r", newline="") as csvfile:
                    csvreader = csv.reader(csvfile)
                    for line in csvreader:
                        try:
                            """
                            This try catch block prevents the program from crashing when it inevitably
                            tries to convert the String header in the csv file to a float
                            """
                            current_total = float(line[-1])
                        except ValueError:
                            current_total = 0.0

                current_total += wage_calculation

                with open("budgetdata.csv", "a", newline="") as csvfile:
                    row = ["Income", f"{wage_calculation:.2f}", "Income", f"{current_total:.2f}"]
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row)

                self.hourlywage_entry.clear()
                self.hoursworked_entry.clear()
            elif self.howmuchincome_entry.text():
                total_income = float(self.howmuchincome_entry.text())
                current_total = 0.0
                with open("budgetdata.csv", "r", newline="") as csvfile:
                    csvreader = csv.reader(csvfile)
                    for line in csvreader:
                        try:
                            current_total = float(line[-1])
                        except ValueError:
                            current_total = 0.0

                current_total += total_income

                with open("budgetdata.csv", "a", newline="") as csvfile:
                    row = ["Income", f"{total_income:.2f}", "Income", f"{current_total:.2f}"]
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row)
                self.howmuchincome_entry.clear()

            budget_amount = 0.0
            with open("budgetdata.csv", "r", newline="") as csvfile:
                csvreader = csv.reader(csvfile)
                for line in csvreader:
                    try:
                        budget_amount = float(line[-1])
                    except ValueError:
                        budget_amount = 0.0

            self.balance_label.setText(f"${budget_amount:.2f}")
            self.budget_message.setText("Report A Change To Your Budget")
        except (ValueError, TypeError):
            self.budget_message.setText("Please Only Enter Numeric Values")

    def submit_expense(self) -> None:
        """
        This function defines what is to occur when clicking the submit button under the expenses tab
        """
        try:
            current_total = 0.0
            expense_amount = float(self.amountofexpense_entry.text())
            with open("budgetdata.csv", "r", newline="") as csvfile:
                csvreader = csv.reader(csvfile)
                for line in csvreader:
                    try:
                        current_total = float(line[-1])
                    except ValueError:
                        current_total = 0.0

            current_total -= expense_amount
            expense_reason = self.expensetype_dropbox.currentText()

            with open("budgetdata.csv", "a", newline="") as csvfile:
                row = ["Expense", f"-{expense_amount:.2f}", expense_reason, f"{current_total:.2f}"]
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row)

            self.balance_label.setText(f"${current_total:.2f}")
            self.budget_message.setText("Report A Change To Your Budget")
        except (ValueError, TypeError):
            self.budget_message.setText("Please Only Enter Numeric Values")
