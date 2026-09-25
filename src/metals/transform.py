import pandas as pd
from datetime import datetime, timezone




def transform_metals(metals_responses: list[dict]) -> pd.DataFrame:
    retrieved_at = datetime.now(timezone.utc)
    data_date = retrieved_at.date()

    records = []

    for metal in metals_responses:
        records.append(
            {
                "metal_name": metal["name"],
                "symbol": metal["symbol"],
                "price": metal["price"],
                "currency": metal["currency"],
                "api_updated_at": pd.to_datetime(metal["updatedAt"],utc=True),
                "retrieved_at": retrieved_at,
                "data_date": data_date,
            }
        )

    metals_df = pd.DataFrame(records)

    return metals_df


