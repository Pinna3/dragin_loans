from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv

from helpers import csv_header, csv_rows_append


def processLoanApplication(start_date, loan_type, loan_amount):
    """
    Creates a loan payment schedule csv file for student and auto loans.
    Acceptable start_date format is '%Y-%m-%d'.
    Loan type can either be auto or student.
    Loan amount must be a positive number.
    """

    # Instantiate datetime for timedelta transformations
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')

    # Set month count at 0, CSV row1 will be the 0th month
    month_count = 0

    # 0th month balance equals the starting loan amount
    remaining_bal = loan_amount

    # csv_rows will be appended with row tuples according to the header schema
    # imported from helpers.py
    csv_rows = []

    # Logic for auto loans
    if loan_type.lower() == "auto":

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
            csv_rows_append(csv_rows, date, incremental_amt_paid, amt_paid_in_interest, amt_paid_towards_princ, remaining_bal)  # noqa:E501

    # Logic for student loans
    elif loan_type.lower() == "student":

        # Starting loan amount must be greater than $5000.00
        if not loan_amount < 5000.01:

            # Initialize reporting values: incremental_amt_paid,
            # amt_paid_in_interest, and amt_paid_towards_princ.
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
                csv_rows_append(csv_rows, date, incremental_amt_paid, amt_paid_in_interest, amt_paid_towards_princ, remaining_bal)  # noqa:E501

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
            csv_rows_append(csv_rows, date, incremental_amt_paid, amt_paid_in_interest, amt_paid_towards_princ, remaining_bal)  # noqa:E501

        # If starting loan amount is not greater than $5000.00 throw a value
        # error.
        else:
            raise ValueError("Loan value must be greater than $5,000.00.")

    # If loan type is not auto or student throw a type error.
    else:
        raise TypeError("Please provide an acceptable loan type.")

    # Generate Loan Payment Schedule CSV file in `csv_payments/ directory w/ a
    # filename composed of the starting date, loan type, and starting loan
    # amount.
    with open(f"csv_payments/{datetime.strftime(start_datetime, '%Y-%m-%d')}_{loan_type}_{loan_amount}.csv", 'w') as file_out:  # noqa:E501
        writer = csv.writer(file_out)
        writer.writerow(csv_header)
        [writer.writerow(csv_row) for csv_row in csv_rows]


# Generate 2 sample csv payment schedules if function is run from main.py
# directly
if __name__ == '__main__':
    processLoanApplication("2021-05-12", "Student", 20000.00)
    processLoanApplication("2021-05-12", "Auto", 20000.00)
