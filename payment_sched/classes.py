from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv
import locale

from helpers import csv_header, csv_rows_append

# Use local currency
locale.setlocale(locale.LC_ALL, '')


class Auto:
    def __init__(self, start_date, loan_amount):
        """
        Student loan payment schedule object.
        Acceptable start_date format is '%Y-%m-%d'.
        Loan amount must be a positive number.
        """

        # csv_rows will be appended with row tuples according to the header
        # schema imported from helpers.py
        self.csv_rows = []

        # Instantiate datetime for timedelta transformations
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')

        # Set month count at 0, CSV row1 will be the 0th month
        month_count = 0

        # 0th month balance equals the starting loan amount
        remaining_bal = loan_amount

        # Apply following logic until loan is paid in full
        while remaining_bal > 0:

            # Date equals starting date + month count
            date = datetime.strftime(start_datetime + relativedelta(months=month_count), '%Y-%m-%d')  # noqa:E501

            # Calculate total amt paid, total interest paid, and principle
            # paid based on month count
            incremental_amt_paid = (.025 * loan_amount) * month_count  # noqa:E501
            amt_paid_in_interest = (.005 * loan_amount) * month_count  # noqa:E501
            amt_paid_towards_princ = (.02 * loan_amount) * month_count  # noqa:E501
            remaining_bal = loan_amount - amt_paid_towards_princ

            # Add another month to month_count
            month_count += 1

            # Append csv row to list
            csv_rows_append(self.csv_rows, date, incremental_amt_paid, amt_paid_in_interest, amt_paid_towards_princ, remaining_bal)  # noqa:E501

        # Set class attributes of potentially useful values like loan_amount,
        # start_date, total_amt_paid, and total_interest_paid
        self.starting_balance = locale.currency(loan_amount, grouping=True)  # noqa:E501
        self.start_date = start_date
        self.total_amt_paid = locale.currency(incremental_amt_paid, grouping=True)  # noqa:E501
        self.total_interest_paid = locale.currency(amt_paid_in_interest, grouping=True)  # noqa:E501

    def generate_csv_payment_schedule(self):
        """
        Generate Loan Payment Schedule CSV file in `csv_payments/ directory
        w/ a filename composed of the starting date, loan type, and starting
        loan amount.
        """
        with open(f"csv_payments/{self.start_date}_Auto_{self.starting_balance}.csv", 'w') as file_out:  # noqa:E501
            writer = csv.writer(file_out)
            writer.writerow(csv_header)
            [writer.writerow(csv_row) for csv_row in self.csv_rows]


class Student:
    def __init__(self, start_date, loan_amount):
        """
        Student loan payment schedule object.
        Acceptable start_date format is '%Y-%m-%d'.
        Loan amount must be a positive number.
        """
        # csv_rows will be appended with row tuples according to the header
        # schema imported from helpers.py
        self.csv_rows = []

        # Instantiate datetime for timedelta transformations
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')

        # Set month count at 0, CSV row1 will be the 0th month
        month_count = 0

        # 0th month balance equals the starting loan amount
        remaining_bal = loan_amount

        # Starting loan amount must be greater than $5000.00
        if not loan_amount < 5000.01:

            # Initialize reporting values: amt_paid_in_interest,
            # amt_paid_towards_princ, and incremental_amt_paid.
            amt_paid_in_interest = 0
            amt_paid_towards_princ = 0
            incremental_amt_paid = 0

            # Apply following logic until loan is paid in full
            while remaining_bal > 0:

                # Date equals starting date + month count
                date = datetime.strftime(start_datetime + relativedelta(months=month_count), '%Y-%m-%d')  # noqa:E501

                # Interest rate is .6% for loan balances > $10,000 and .4% for
                # loan balances <= $10,000.
                interest_rate = .006 if remaining_bal > 10_000.00 else .004

                # Append csv row to list for remaining balances > $1000
                csv_rows_append(self.csv_rows, date, incremental_amt_paid, amt_paid_in_interest, amt_paid_towards_princ, remaining_bal)  # noqa:E501

                # Calculate total amt paid, total interest paid, principle
                # paid, and remaining balance based on monthly accumulating
                # interest. Add caveats for last month where only the balance
                # is due and no additional interest is accumulated.
                new_balance = remaining_bal * (1 + interest_rate) if remaining_bal > 1000 else remaining_bal  # noqa:E501
                incremental_amt_paid += 1000 if remaining_bal > 1000 else remaining_bal  # noqa:E501
                amt_paid_in_interest += remaining_bal * interest_rate if remaining_bal > 1000 else 0  # noqa:E501
                amt_paid_towards_princ = incremental_amt_paid - amt_paid_in_interest  # noqa:E501
                remaining_bal = new_balance - 1000 if remaining_bal > 1000 else 0  # noqa:E501
                month_count += 1

            # Append csv row for last month where only the balance is due and
            # no additional interest is accumulated.
            date = datetime.strftime(start_datetime + relativedelta(months=month_count), '%Y-%m-%d')  # noqa:E501
            csv_rows_append(self.csv_rows, date, incremental_amt_paid, amt_paid_in_interest, amt_paid_towards_princ, remaining_bal)  # noqa:E501

        # If starting loan amount is not greater than $5000.00 throw a value
        # error.
        else:
            raise ValueError("Loan value must be greater than $5,000.00.")

        # Set class attributes of potentially useful values like loan_amount,
        # start_date, total_amt_paid, and total_interest_paid
        self.starting_balance = locale.currency(loan_amount, grouping=True)  # noqa:E501
        self.start_date = start_date
        self.total_amt_paid = locale.currency(incremental_amt_paid, grouping=True)  # noqa:E501
        self.total_interest_paid = locale.currency(amt_paid_in_interest, grouping=True)  # noqa:E501

    def generate_csv_payment_schedule(self):
        """
        Generate Loan Payment Schedule CSV file in `csv_payments/ directory
        w/ a filename composed of the starting date, loan type, and starting
        loan amount.
        """
        with open(f"csv_payments/{self.start_date}_Student_{self.starting_balance}.csv", 'w') as file_out:  # noqa:E501
            writer = csv.writer(file_out)
            writer.writerow(csv_header)
            [writer.writerow(csv_row) for csv_row in self.csv_rows]


# Generate 2 x sample csv payment schedules if classes.py is executed
if __name__ == '__main__':
    loan = Auto('2022-06-15', 15_000.00)
    loan.generate_csv_payment_schedule()

    print('Auto:')
    print('Start Date: ', loan.start_date)
    print('Starting Balance: ', loan.starting_balance)
    print('Total Amount Paid: ', loan.total_amt_paid)
    print('Total Interest Paid: ', loan.total_interest_paid)

    print("\n")
    loan = Student('2022-06-15', 15_000.00)
    loan.generate_csv_payment_schedule()

    print('Student:')
    print('Start Date: ', loan.start_date)
    print('Starting Balance: ', loan.starting_balance)
    print('Total Amount Paid: ', loan.total_amt_paid)
    print('Total Interest Paid: ', loan.total_interest_paid)
