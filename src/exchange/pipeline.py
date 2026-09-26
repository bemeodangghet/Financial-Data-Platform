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

    # Extract
    exchange_response = fetch_exchange_rates()

    # Validate
    validate_exchange_response(exchange_response)

    # Transform
    exchange_rates_df = transform_exchange_rates(exchange_response)

    # Save CSV backup
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/processed/exchange_rates/exchange_rates_{timestamp}.csv"

    save_csv(exchange_rates_df, file_path)

    logger.info("Data saved successfully to %s", file_path)

    # Load to PostgreSQL
    engine = get_engine()

    save_to_postgres(
        df=exchange_rates_df,
        table_name="exchange_rates",
        engine=engine,
        constraint_name="unique_daily_rate",
    )

    logger.info("Exchange rate pipeline completed successfully.")