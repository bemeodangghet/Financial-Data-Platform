import requests

from metals.settings_metals import (
    METALS_API_URL,
    METAL_SYMBOLS,
    REQUEST_TIMEOUT,
)


def fetch_metals() -> list[dict]:
    metals_responses = []

    for symbol in METAL_SYMBOLS:
        response = requests.get(
            f"{METALS_API_URL}/{symbol}",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        metals_response = response.json()
        metals_responses.append(metals_response)

    return metals_responses