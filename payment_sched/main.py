from classes import Auto, Student


def processLoanApplication(start_date, loan_type, loan_amount):
    """
    Generates a loan payment schedule CSV file for auto or student loans.
    Acceptable start_date format is '%Y-%m-%d'.
    Loan type can either be auto or student (Not case sensitive).
    Loan amount must be a positive number.
    """

    # Generate auto loan payment schedule
    if loan_type.lower() == "auto":

        # Instantiate auto object
        loan = Auto(start_date, loan_amount)

        # Log noteworthy auto loan attributes
        print('Auto:')
        print('Start Date: ', loan.start_date)
        print('Starting Balance: ', loan.starting_balance)
        print('Total Amount Paid: ', loan.total_amt_paid)
        print('Total Interest Paid: ', loan.total_interest_paid)

        # Generate auto loan payment schedule csv file
        loan.generate_csv_payment_schedule()

    # Generate student loan Payment schedule
    elif loan_type.lower() == "student":

        # Instantiate student object
        loan = Student(start_date, loan_amount)

        # Log noteworthy student loan attributes
        print('Student:')
        print('Start Date: ', loan.start_date)
        print('Starting Balance: ', loan.starting_balance)
        print('Total Amount Paid: ', loan.total_amt_paid)
        print('Total Interest Paid: ', loan.total_interest_paid)

        # Generate student loan payment schedule csv file
        loan.generate_csv_payment_schedule()

    # If loan type is not auto or student throw a type error.
    else:
        raise TypeError("Please provide an acceptable loan type.")


# Generate 2 x sample csv payment schedules if main.py is executed
if __name__ == '__main__':
    processLoanApplication("2021-05-12", "Student", 20000.00)
    processLoanApplication("2021-05-12", "Auto", 20000.00)
