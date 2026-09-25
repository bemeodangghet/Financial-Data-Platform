import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert

from core.logger import get_logger


load_dotenv()

logger = get_logger(__name__)


def get_engine():
    """Create PostgreSQL engine."""

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")

    return create_engine(database_url)


def save_to_postgres(
    df,
    table_name: str,
    engine,
    constraint_name: str,
) -> None:
    """Insert DataFrame records into PostgreSQL and skip duplicates."""

    metadata = MetaData()
    table = Table(
        table_name,
        metadata,
        autoload_with=engine,
    )

    records = df.to_dict(orient="records")

    if not records:
        logger.warning(f"No data to insert into '{table_name}'.")
        return

    stmt = insert(table).values(records)

    stmt = stmt.on_conflict_do_nothing(
        constraint=constraint_name
    )

    with engine.begin() as connection:
        result = connection.execute(stmt)

    inserted = result.rowcount
    total = len(records)
    skipped = total - inserted

    if inserted == 0:
        logger.info(
            f"No new records inserted into '{table_name}'. "
            f"All {total} records already exist."
        )
    else:
        logger.info(
            f"Inserted {inserted} records into '{table_name}', "
            f"skipped {skipped} duplicates."
        )