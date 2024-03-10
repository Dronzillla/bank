from dataclasses import dataclass, field
from typing import ClassVar
from conversion import CurrencyConversion
import csv
from abc import ABC, abstractmethod

# For logger
from logg import setup_logging
import logging.config
import logging.handlers

# Use logger based on module name
logger = logging.getLogger(__name__)


@dataclass
class BankAccount(ABC):
    name: str
    balance: float
    currency: str
    id: int = field(repr=True)
    account_type: str = field(repr=True)

    @abstractmethod
    def make_class_abstract(self) -> None:
        pass


@dataclass
class StandardBankAccount(BankAccount):
    data_field: int = field(default=0, init=False, repr=False)

    def make_class_abstract(self) -> None:
        pass


@dataclass
class PremiumBankAccount(BankAccount):
    data_field: int = field(default=0, init=False, repr=False)

    def make_class_abstract(self) -> None:
        pass


@dataclass
class BankAccountManager:
    all: list["BankAccount"] = field(default_factory=list, init=False)
    # ids: list = field(default_factory=list, init=False)
    last_id: int = field(default=1, init=False)

    def dump_accounts_to_csv(self) -> None:
        fname = "data_accounts.csv"
        with open(fname, "w") as wfile:
            writer = csv.writer(wfile, delimiter=",")
            writer.writerow(["name", "balance", "currency"])
            for account in self.all:
                logger.info(f"Writing to file: {account}")
                writer.writerow([account.name, account.balance, account.currency])

    def search_account_by_id(self, id: int) -> "BankAccount":
        for account in self.all:
            if account.id == id:
                return account

    def create_account(
        self, name: str, balance: float, currency: str, account_type: str
    ) -> None:
        if account_type == "STD":
            account = StandardBankAccount(
                name=name,
                balance=balance,
                currency=currency,
                id=self.last_id,
                account_type=account_type,
            )
        elif account_type == "PRM":
            account = PremiumBankAccount(
                name=name,
                balance=balance,
                currency=currency,
                id=self.last_id,
                account_type=account_type,
            )

        # Append to all list and update last id
        self.all.append(account)
        self.last_id += 1

    def delete_account(self, id: int) -> None:
        account_to_delete = self.search_account_by_id(id)
        index_account_to_delete = self.all.index(account_to_delete)
        self.all.pop(index_account_to_delete)

    def deposit(self, id: int, amount: float):
        account = self.search_account_by_id(id)
        account.balance += amount

    def withdraw(self, id: int, amount: float):
        fee = amount * 0.5 / 100
        account = self.search_account_by_id(id)
        # Maybe we need validation to check if money left to withdraw
        account.balance -= amount + fee

    def transfer(self, id1: int, id2: int, amount: float):
        account_minus = self.search_account_by_id(id1)
        account_plus = self.search_account_by_id(id2)

        # Adjust balance of first account
        fee = amount * 0.7 / 100
        account_minus.balance -= amount + fee
        # Get currencies of both accounts
        account_minus_currency = account_minus.currency
        account_plus_currency = account_plus.currency
        # Adjust balance of second account
        ratio = CurrencyConversion.convert_currency(
            account_minus_currency, account_plus_currency
        )
        account_plus.balance += amount * ratio

    def parse_records(self, records: list[list]) -> None:
        for record in records:
            self.parse_record(record)

    def parse_record(self, record: list) -> None:
        command = record[0]

        if command == "CREATE_ACC_STD":
            name = record[1]
            balance = float(record[2])
            currency = record[3]
            self.create_account(name, balance, currency, "STD")

        elif command == "CREATE_ACC_PRM":
            name = record[1]
            balance = float(record[2])
            currency = record[3]
            self.create_account(name, balance, currency, "PRM")

        elif command == "DELETE_ACC":
            id = int(record[1])
            self.delete_account(id)

        elif command == "DEPOSIT":
            id = int(record[1])
            amount = float(record[2])
            self.deposit(id, amount)

        elif command == "WITHDRAW":
            id = int(record[1])
            amount = float(record[2])
            self.withdraw(id, amount)

        elif command == "TRANSFER":
            id1 = int(record[1])
            id2 = int(record[2])
            amount = float(record[3])
            self.transfer(id1, id2, amount)

        else:
            logger.warning(f"Unable to parse record. Invalid command entered.")


def main() -> None:
    setup_logging()


if __name__ == "__main__":
    main()
