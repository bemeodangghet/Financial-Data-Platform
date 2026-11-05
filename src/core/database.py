
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert

from core.logger import get_logger


if os.getenv("RUNNING_IN_DOCKER") != "true":
    load_dotenv(".env.local", override=True)

logger = get_logger(__name__)


# Create engine
def get_engine():
    """Create PostgreSQL engine."""

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"]
    )

    return create_engine(
        db_url,
        pool_pre_ping=True
    )


# Load data to database
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
