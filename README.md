Build an application in Python that is run with a single function called
processLoanApplication(start_date, loan_type, loan_amount)
The function should output a CSV file with a payback schedule that shows each month’s
payback in the following columns:
1. DATE
2. INCREMENTAL AMOUNT PAID
3. AMOUNT PAID IN INTEREST
4. AMOUNT PAID TOWARDS PRINCIPAL
5. REMAINING LOAN BALANCE

Within your code you should allow two loan CLASSES: &quot;Auto&quot; and &quot;Student&quot;.

Auto loans have the following unique properties:
 .5% interest is charged each month on the original loan amount.
 Each month 2.5% of the original loan amount is due. First the .5% interest is paid, and then the
remaining money pays down the principal. Once there is no principal remaining the loan is
completed.
 The final month can pay whatever is the remaining balance
Example:
$20,000 loan
.005 * 20,000 = $100 interest each month
First payment: .025 * 20,000 = $500, $100 goes to interest, the other $400 to principal.
The next month the loan would look like this:
Original loan: $20,000
Remaining principal: $19,600
$100 interest due
$500 monthly payment due

Student Loans have the following property:
 Minimum loan amount of $5,000
 .4% monthly interest if loan balance is $10,000 or less
 .6% monthly interest is remaining loan balance is &gt; $10,000
 Monthly payments are a flat $1,000 until the loan is paid in full.
 The final month can pay whatever is due.
