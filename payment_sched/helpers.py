import locale

# Use local currency
locale.setlocale(locale.LC_ALL, '')

# CSV Header
csv_header = [
    "DATE",
    "INCREMENTAL AMOUNT PAID",
    "AMOUNT PAID IN INTEREST",
    "AMOUNT PAID TOWARDS PRINCIPLE",
    "REMAINING LOAN BALANCE"
]


def csv_rows_append(csv_rows, date, incremental_amt_paid, amt_paid_in_interest, amt_paid_towards_princ, remaining_bal):  # noqa:E501
    # Factor out list appending tuple logic to avoid annoying repeats in main
    # function processLoanApplication()
    csv_rows.append(
        (
            date,
            locale.currency(incremental_amt_paid, grouping=True),
            locale.currency(amt_paid_in_interest, grouping=True),
            locale.currency(amt_paid_towards_princ, grouping=True),
            locale.currency(remaining_bal, grouping=True)
        )
    )
