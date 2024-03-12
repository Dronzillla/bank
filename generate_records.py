from random import choice, randint
from dataclasses import dataclass, field
from random_words import RandomNicknames
from accounts import BankAccountManager


@dataclass
class Record:
    text: str = field()


@dataclass
class RecordManager:
    bank_account_manager: BankAccountManager = field(default=BankAccountManager())
    all_records: list = field(default_factory=list)

    def get_random_name(self) -> str:
        rn = RandomNicknames()
        name = rn.random_nick(gender="u")
        surname = rn.random_nick(gender="u")
        fullname = name + " " + surname
        return fullname

    def get_random_balance(self) -> int:
        balance = randint(0, 2500)
        return balance

    def get_random_amount(self) -> int:
        amount = randint(0, 250)
        return amount

    def get_random_currency(self) -> str:
        currencies = ["EUR", "USD", "GBP"]
        currency = choice(currencies)
        return currency

    # Get a list of created account ids
    def get_bank_account_ids(self) -> list:
        ids = []
        for account in self.bank_account_manager.all:
            ids.append(account.id)
        return ids

    def parse_command(self, command: str) -> None:
        # Parse the command acordingly
        if command == "CREATE_ACC_STD":
            name = self.get_random_name()
            balance = self.get_random_balance()
            currency = self.get_random_currency()
            account_type = "STD"

            self.bank_account_manager.create_account(
                name=name, balance=balance, currency=currency, account_type=account_type
            )
            # TODO Write to .txt file
            self.all_records.append(command + name)

        elif command == "CREATE_ACC_PRM":
            name = self.get_random_name()
            balance = self.get_random_balance()
            currency = self.get_random_currency()
            account_type = "PRM"
            self.bank_account_manager.create_account(
                name=name, balance=balance, currency=currency, account_type=account_type
            )

            self.all_records.append(command + name)

        elif command == "DELETE_ACC":
            # Get random bank id
            # And delete it if it exists
            ids = self.get_bank_account_ids()
            id = choice(ids)
            self.bank_account_manager.delete_account(id=id)

            self.all_records.append(command + name)

        elif command == "DEPOSIT":
            # Get random bank id
            # And deposit money to that bank account
            ids = self.get_bank_account_ids()
            amount = self.get_random_amount()
            id = choice(ids)
            self.bank_account_manager.deposit(id, amount)

            self.all_records.append(command + name)

        elif command == "WITHDRAW":
            # Get random bank id
            ids = self.get_bank_account_ids()
            amount = self.get_random_amount()
            id = choice(ids)
            self.bank_account_manager.withdraw(id, amount)

            self.all_records.append(command + name)


def random_command() -> str:
    # Get random command
    commands = [
        "CREATE_ACC_STD",
        "CREATE_ACC_PRM",
        "DELETE_ACC",
        "DEPOSIT",
        "WITHDRAW",
    ]
    command = choice(commands)
    return command


def main():
    record_manager = RecordManager()

    counter = 0
    while True:
        # Break condition for while loop
        if counter == 10:
            break

        # Get random command
        command = random_command()

        # Try to add this to records
        try:
            record_manager.parse_command(command)
            counter += 1
        except IndexError:
            continue


if __name__ == "__main__":
    main()
