class CurrencyConversion:
    RATES = {
        "EUR": {"USD": 1.09, "GBP": 0.85, "EUR": 1},
        "USD": {"EUR": 0.91, "GBP": 0.78, "USD": 1},
        "GBP": {"USD": 1.28, "EUR": 1.17, "GBP": 1},
    }

    @staticmethod
    def convert_currency(currency1: str, currency2: str) -> float:
        try:
            rate = CurrencyConversion.RATES[currency1][currency2]
            return rate
        except KeyError:
            # Implement logging maybe?
            return 1


def main():
    ...
    # For testing
    # rate = CurrencyConversion.convert_currency("EUR", "USD")
    # print(rate)


if __name__ == "__main__":
    main()
