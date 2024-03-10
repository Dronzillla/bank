from dataclasses import dataclass, field
from typing import Union
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
    name: str = field(repr=True)
    balance: float = field(repr=True)
    currency: str = field(repr=True)
    id: int = field(repr=True)
    account_type: str = field(repr=True)

    def round_balance(self) -> None:
        self.balance = round(self.balance, 2)

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.round_balance()

    @abstractmethod
    def withdraw(self) -> None:
        pass

    @abstractmethod
    def transfer(self) -> None:
        pass


@dataclass
class StandardBankAccount(BankAccount):
    # Dataclasses won't automatically consider attributes defined in the base class, so field function is created
    data_field: int = field(default=0, init=False, repr=False)

    # After creating the account deduct a fee for account creation 0.1% of initial funds
    def __post_init__(self) -> None:
        if self.balance != 0:
            fee = 0.1 / 100 * self.balance
            self.balance -= fee
            self.round_balance()

    def withdraw(self, amount: float) -> None:
        fee = amount * 0.5 / 100
        self.balance -= amount + fee
        self.round_balance()

    def transfer(self, amount: float, party: str) -> None:
        if party == "sender":
            fee = amount * 0.7 / 100
            self.balance -= amount + fee
        elif party == "receiver":
            self.balance += amount
        self.round_balance()


@dataclass
class PremiumBankAccount(BankAccount):
    # Dataclasses won't automatically consider attributes defined in the base class, so field function is created
    data_field: int = field(default=0, init=False, repr=False)

    # After creating the account deduct a fee for account creation 0.3% of initial funds
    def __post_init__(self) -> None:
        if self.balance != 0:
            fee = 0.3 / 100 * self.balance
            self.balance -= fee
            self.round_balance()

    def withdraw(self, amount: float) -> None:
        fee = amount * 0.3 / 100
        self.balance -= amount + fee
        self.round_balance()

    def transfer(self, amount: float, party: str) -> None:
        if party == "sender":
            fee = amount * 0.45 / 100
            self.balance -= amount + fee
        elif party == "receiver":
            self.balance += amount
        self.round_balance()


@dataclass
class BankAccountManager:
    all: list[Union[StandardBankAccount, PremiumBankAccount]] = field(
        default_factory=list, init=False
    )
    last_id: int = field(default=1, init=False)

    def dump_accounts_to_csv(self) -> None:
        fname = "data_accounts.csv"
        with open(fname, "w") as wfile:
            writer = csv.writer(wfile, delimiter=",")
            writer.writerow(["account_id", "holder", "balance", "currency"])
            for account in self.all:
                logger.info(f"Writing to file: {account}")
                account_str = "'" + account.name + "'"
                writer.writerow(
                    [account.id, account_str, account.balance, account.currency]
                )

    def search_account_by_id(
        self, id: int
    ) -> Union[StandardBankAccount, PremiumBankAccount]:
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

    def deposit(self, id: int, amount: float) -> None:
        account = self.search_account_by_id(id)
        account.deposit(amount)

    def withdraw(self, id: int, amount: float) -> None:
        account = self.search_account_by_id(id)
        account.withdraw(amount)

    def transfer(self, id1: int, id2: int, amount: float) -> None:
        # Get accounts for sender and receiver of funds
        account_sender = self.search_account_by_id(id1)
        account_receiver = self.search_account_by_id(id2)

        # Get currencies of both accounts
        account_sender_currency = account_sender.currency
        account_receiver_currency = account_receiver.currency
        # Calculate currency ratio for receiver account currency
        ratio = CurrencyConversion.convert_currency(
            account_sender_currency, account_receiver_currency
        )
        # Adjust balance for both accounts: receiver (+) or sender (-)
        account_sender.transfer(amount, "sender")
        account_receiver.transfer(amount * ratio, "receiver")

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
