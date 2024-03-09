import bank_records
from accounts import BankAccountManager


def main() -> None:
    # Get a list of records
    records = bank_records.main()

    # Parse each record and dump information about accounts in csv
    manager = BankAccountManager()
    manager.parse_records(records)
    manager.dump_acounts_to_csv()

    # For testing (print the result) to console
    for account in manager.all:
        print(account)


if __name__ == "__main__":
    main()
