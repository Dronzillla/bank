from bank_records import setup_logging
import logging.config
import logging.handlers

# Use logger based on module name
logger = logging.getLogger(__name__)


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
            # logger.info(f"{currency1} converted to {currency2}. Exchange rate: {rate}.")
            return rate
        except KeyError:
            logger.warning(
                f"No conversion rate for currencies {currency1} and {currency2}."
            )
            return 1


def main() -> None:
    setup_logging()

    # For testing
    # rate = CurrencyConversion.convert_currency("EUR", "USD")
    # print(rate)


if __name__ == "__main__":
    main()
