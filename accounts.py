from dataclasses import dataclass, field
import bank_records
from typing import ClassVar


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
    all: list["BankAccount"] = field(default_factory=list)
    ids: list = field(default_factory=list)

    def create_account(self, record: list): ...

    def delete_account(self, id: int): ...

    def deposit(self, id: int, number: float): ...

    def withdraw(self, id: int, number: float): ...

    def transfer(self, id1: int, id2: int, number: float): ...

    def parse_records(self, records: list[list]): ...

    def parse_record(self, record: list): ...


def main():
    # records = bank_records.main()
    # for record in records:
    #     print(record)

    acc1 = BankAccount("Peter Wonker", 0, "USD")
    acc2 = BankAccount("John Walker", 100, "EUR")

    print(acc1.id)
    print(acc2.id)


if __name__ == "__main__":
    main()
