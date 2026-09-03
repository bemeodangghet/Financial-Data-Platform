import pandas as pd
from datetime import datetime


def transform_exchange_rates(exchange_response: dict) -> pd.DataFrame:
    base_currency = exchange_response["base_code"]
    exchange_rates = exchange_response["rates"]
    api_updated_at = exchange_response["time_last_update_utc"]

    retrieved_at = datetime.utcnow()
    data_date = retrieved_at.date()

    records = []

    for target_currency, exchange_rate in exchange_rates.items():

        records.append(
            {
                "base_currency": base_currency,
                "target_currency": target_currency,
                "exchange_rate": exchange_rate,
                "api_updated_at": api_updated_at,
                "retrieved_at": retrieved_at,
            }
        )

    exchange_rates_df = pd.DataFrame(records)

    # convert datetime
    exchange_rates_df["api_updated_at"] = pd.to_datetime(
        exchange_rates_df["api_updated_at"]
    )

    # DATA QUALITY CHECK
    if exchange_rates_df["exchange_rate"].isnull().any():
        raise ValueError("Missing exchange rate")

    if (exchange_rates_df["exchange_rate"] <= 0).any():
        raise ValueError("Invalid exchange rate")

    # add data_date
    exchange_rates_df["data_date"] = data_date

    return exchange_rates_df


    

