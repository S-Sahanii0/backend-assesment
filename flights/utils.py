import re

from requests import get


def make_request(url: str) -> dict:
    """Creates a simple GET request to the given url and returns the response as a dict."""

    return get(url).json()


def split_currency_and_amount(price: str) -> tuple[str, str]:
    """Splits the given price string into currency and amount.
    eg: '$100' -> ('$', '100')"""

    vals = re.split(r'(\d+)', price)
    return vals[0], vals[1]
