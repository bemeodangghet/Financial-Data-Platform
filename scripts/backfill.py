import os

import pandas as pd

from core.database import save_to_postgres
from core.database import get_engine


def backfill_csv(folder_path: str):
    engine = get_engine()

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)

            print(f"exchange {file}...")

            df = pd.read_csv(file_path)

            # Convert datetime
            df["retrieved_at"] = pd.to_datetime(df["retrieved_at"])

            # Add data_date
            df["data_date"] = df["retrieved_at"].dt.date

            # Deduplicate
            df = df.drop_duplicates(
                subset=["base_currency", "target_currency", "data_date"]
            )

            save_to_postgres(df, "exchange_rates", engine)

            print(f"Loaded {file}")


if __name__ == "__main__":
    backfill_csv("data/processed")