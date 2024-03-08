from dataclasses import dataclass, field
import bank_records
from typing import ClassVar
from typing import Generator


@dataclass
class BankAccount:
    name: str = field()
    balance: float = field()
    currency: str = field()

    # Make a class attribute to count instances
    ids: ClassVar = field(init=False, default=[])

    def __post_init__(self):
        if len(self.ids) == 0:
            self.id = 1
        else:
            self.id = self.ids[-1] + 1
        self.ids.append(self.id)


@dataclass
class BankAccountManager:
    all: list["BankAccount"] = field(default_factory=list, init=False)
    # ids: list = field(default_factory=list, init=False)

    def is_balance_too_low(self): ...

    def search_account_by_id(self, id: int) -> "BankAccount":
        for account in self.all:
            if account.id == id:
                return account

    def create_account(self, name: str, balance: float, currency: str) -> None:
        self.all.append(BankAccount(name, balance, currency))

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

    def transfer(self, id1: int, id2: int, amount: float): ...

    def parse_records(self, records: list[list]) -> None:
        for record in records:
            self.parse_record(record)

    def parse_record(self, record: list) -> None:
        command = record[0]

        if command == "CREATE_ACC":
            name = record[1]
            balance = float(record[2])
            currency = record[3]
            self.create_account(name, balance, currency)

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
            # self.transfer(id1, id2, amount)

        else:
            ...


def main():
    records = bank_records.main()

    manager = BankAccountManager()
    manager.parse_records(records)

    for account in manager.all:
        print(account)

    # acc1 = BankAccount("Peter Wonker", 0, "USD")
    # acc2 = BankAccount("John Walker", 100, "EUR")

    # print(acc1.id)
    # print(acc2.id)


if __name__ == "__main__":
    main()
