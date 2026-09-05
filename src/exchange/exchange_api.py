import requests
from exchange.settings_exchange import (
    EXCHANGE_RATE_API_URL,
    REQUEST_TIMEOUT,
)

#get data from exchange rate api
def fetch_exchange_rates() -> dict:
    response = requests.get(EXCHANGE_RATE_API_URL, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    return response.json()