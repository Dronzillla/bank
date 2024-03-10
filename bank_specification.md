## Bank simulation (D)

Your tasks is to build a system that can parse bank records and put them into a "database" correctly. 
We will not work with actual databases, but will represent them as classes and files.

Consider the following text file (copy and save it as `bank-records.txt`) consisting of these bank records:
```
CREATE_ACC "John Smith" 0 EUR
DEPOSIT 1 200
WITHDRAW 1 100
CREATE_ACC "Louise Johnson" 500 USD
WITHDRAW 1 50
WITHDRAW 2 25
TRANSFER 2 1 100
DELETE_ACC 2
CREATE_ACC "John Smith" 1000 USD
CREATE_ACC "Peter W Higgs" 123 GBP
TRANSFER 3 4 100
```

Explanation:
-  `CREATE_ACC "John Smith" 0 EUR`. Creates an account for "John Smith" with an initial balance of 0 for EUR currency. 
  - Upon creation, an automatic ID starting (from 1 and incrementing by 1 for each new account) should be assigned to each account which will be referred to in the next commands.
- `DEPOSIT 1 200`. Add 200 money (whichever currency the account has) to the account with ID 1 (the only one that has been created so far)
- `WITHDRAW 1 100`. Subtract 100 money from account with ID 1. Subtract an extra 0.5% from the withdrawal amount (in this case, 2.5 EUR) because the bank charges for withdrawal.   
- `CREATE_ACC "Louise Johnson" 500 USD`. Create a new account for holder "Louis Johnson" with an initial balance of 500 USD
- `WITHDRAW 1 50`. Subtract 50 money from account with ID 1. Subtract an extra 0.5% from the withdrawal amount because the bank charges for withdrawal. 
- `WITHDRAW 2 25`. Subtract 25 money from account 25. Subtract an extra 0.5% from the withdrawal amount because the bank charges for withdrawal. 
- `TRANSFER 2 1 100`. Transfer 100 money from account 2 to account 1. 
  - Since account 2 has currency USD, we will transfer 100 USD to account 1. 
  - Proper currency conversion should take place when transferring between accounts with different currencies. 
  - Transfers cost 0.7% of (in this case, 0.7 USD) the transferred amount for the account sending money (in this case, account ID 2).
- `DELETE_ACC 2`. The account with ID 2 should be deleted from the bank system. New account ids continue to increment UP.
- `CREATE_ACC "John Smith" 1000 USD`. Creates an account for "John Smith" with an initial balance of 1000 for USD currency. 
- `CREATE_ACC "Peter W Higgs" 123 GBP`. Creates an account for "Peter Higgs" with an initial balance of 123 CHF currency. 
- `TRANSFER 3 4 100`. Transfer 100 money (of corresponding currency) from account 3 to account 4.  
  
In a nutshell, your task is to:
- Create a way to read the file, parse the bank records and handle them accordingly
- You should use classes to handle storage of data for accounts and processing the transactions
- At the end of reading the whole file and handling its operations, you should print the final states of all _existing_ accounts to a CSV file

### Stage 1

- Create a file `main.py` which will be the starting file to our application
- As always, add `if __name__ == "__main__":` in it which is where we will trigger the necessary functions to process the bank records file
- Create a file `bank_records.py` where we will store all bank record reading information  
- Implement a function to read the file `bank-records.txt` line by line
- Process each word of the input by splitting it up by spaces. Hint: take a look at the `csv` library and its `delimeter` parameter, it could save you a lot of trouble.
- For debugging, use the `logging` library to log how the bank record was parsed. For example:
```
2024-02-27 20:41:52,157 DEBUG. Command: CREATE_ACC, Parameters: ['John Smith', '0', 'EUR']
2024-02-27 20:41:52,157 DEBUG. Command: DEPOSIT, Parameters: ['1', '200']
2024-02-27 20:41:52,157 DEBUG. Command: WITHDRAW, Parameters: ['1', '100']
```

### Stage 2

- Create an `accounts.py` file and keep all account-related classes here
- Create a `BankAccount` dataclass that has all the needed properties
- Create a `BankAccountManager` class that holds a list of all `BankAccount` instances created and performs all the appropriate operations on them
  - For now, skip handling the `TRANSFER` operation
- For debugging, log the string representation of each account before and after the bank command action was taken. For example:
```
2024-02-27 20:55:36,070 DEBUG. BankAccount(id=1, holder='John Smith', balance=0, currency='EUR')
2024-02-27 20:55:36,070 DEBUG. Performing deposit on account id 1 with amount 200
2024-02-27 20:55:36,070 DEBUG. BankAccount(id=1, holder='John Smith', balance=200, currency='EUR')
```

### Stage 3

- Create a `conversion.py` file and keep the currency conversion-related things here
- Create a `CurrencyConversion` class which 
  - Has a dictionary with currencies (in our example it's enough to have EUR, USD, GBP) and their conversion rates. Use the following conversion rates:
    - USD to EUR: 0.91
    - EUR to USD: 1.09
    - USD to GBP: 0.78
    - GBP to USD: 1.28
    - EUR to GBP: 0.85
    - GBP to EUR: 1.17
  - Has a method `convert_currency` that converts a given amount of one currency to a different currency
- Implement the `TRANSFER` command handling using the `CurrencyConversion` class instance

### Stage 4

- Implement a method `dump_accounts_to_csv` as part of `BankAccountManager` which writes the state of each _still existing_ account to a csv file. For example, after processing the file above, our output CSV file should look like this:
```csv
account_id,holder,balance,currency
1,"John Smith",140.25,EUR
3,"John Smith",899.3,USD
4,"Peter W Higgs",201.00,GBP
```
- Add another debug logging when writing to file, for example
```
2024-02-27 20:59:56,080 DEBUG. Writing to file: BankAccount(id=1, holder='John Smith', balance=200, currency='EUR')
```

### (Advanced) Stage 5 

- Extend the bank record format so that now there's two types of accounts: standard and premium.
  - For example, the command `CREATE_ACC_STD "ABC" 100 USD` will create a standard account for account holder ABC with 100 USD initial funds.
  - The command `CREATE_ACC_PRM` would create a premium account
- Reflect these changes by changing `BankAccount` to an abstract base class.
  - Extend `BankAccount` class to implement with additional `account_type` property.
  - Implement `StandardBankAccount` and `PremiumBankAccount`, both inherit from `BankAccount`
  - Change the withdrawal and transfer methods in `BankAccount` to be abstract methods, concrete implementations of these methods should reside in `PremiumBankAccount` and `StandardBankAccount` instead
    - Standard accounts, as before, pay 0.5% for money withdrawal and 0.7% for money transfers
    - Premium accounts pay 0.3% for money withdrawal and 0.45% for money transfers
    - When created, standard accounts pay 0.1% of their initial funds for the account creation (if the initial funds are 0, then they don't pay anything)
    - When created, premium accounts pay 0.3% of their initial funds for the account creation (if the initial funds are 0, then they don't pay anything)
- Update the logging messages to reflect these changes
- When writing the final result to CSV file, also include the account type

So, after incorporating these changes and processing the following bank records:
```
CREATE_ACC_STD "John Smith" 0 EUR
DEPOSIT 1 200
WITHDRAW 1 100
CREATE_ACC_PRM "Louise Johnson" 500 USD
WITHDRAW 1 50
WITHDRAW 2 25
TRANSFER 2 1 100
DELETE_ACC 2
CREATE_ACC_PRM "John Smith" 1000 USD
CREATE_ACC_STD "Peter W Higgs" 123 GBP
TRANSFER 3 4 100
```

the final CSV output file should look like:
```csv
account_id,holder,balance,currency
1,"John Smith",140.25,EUR
3,"John Smith",896.55,USD
4,"Peter W Higgs",200.88,GBP
```
