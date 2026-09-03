from datetime import datetime

from exchange.exchange_api import fetch_exchange_rates
from exchange.validation import validate_exchange_response
from exchange.transform import transform_exchange_rates

from core.database import get_engine, save_to_postgres
from core.file_handler import save_csv
from core.logger import get_logger


logger = get_logger(__name__)


def run_exchange_pipeline() -> None:
    logger.info("Starting exchange rate pipeline...")

    exchange_response = fetch_exchange_rates()

    validate_exchange_response(exchange_response)

    exchange_rates_df = transform_exchange_rates(exchange_response)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/processed/exchange_rates_{timestamp}.csv"

    save_csv(exchange_rates_df, file_path)

    logger.info("Data saved successfully to %s", file_path)

    engine = get_engine()

    save_to_postgres(
        exchange_rates_df,
        "exchange_rates",
        engine,
    )

    logger.info("Exchange rate pipeline completed successfully.")