from datetime import datetime

from metals.metals_api import fetch_metals
from metals.metals_validation import validate_metals_response
from metals.transform import transform_metals

from core.database import get_engine, save_to_postgres
from core.file_handler import save_csv
from core.logger import get_logger


logger = get_logger(__name__)


def run_metals_pipeline() -> None:
    logger.info("Starting metals pipeline...")

    # Extract
    metals_responses = fetch_metals()

    # Validate
    validate_metals_response(metals_responses)

    # Transform
    metals_df = transform_metals(metals_responses)    

    # Save CSV backup
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/processed/metals/metals_{timestamp}.csv"

    save_csv(metals_df, file_path)
    
    logger.info("Data saved successfully to %s", file_path)

    # Load to PostgreSQL
    engine = get_engine()

    save_to_postgres(
        df=metals_df,
        table_name="metal_prices",
        engine=engine,
        constraint_name="unique_daily_metal_price",
    )

    logger.info("Metals pipeline completed successfully.")