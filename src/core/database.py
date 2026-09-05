from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.postgresql import insert

from core.logger import get_logger

#Create engine
def get_engine():
    """ Create PostgreSQL engine """
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5432/Financial Data Platform"
    )

    return engine

logger = get_logger(__name__)

#Load data to postgres
def save_to_postgres(df, table_name, engine):
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)

    records = df.to_dict(orient="records")

    if not records:
        logger.warning("No data to insert.")
        return

    stmt = insert(table).values(records)

    stmt = stmt.on_conflict_do_nothing(
        constraint="unique_daily_rate"
    )

    with engine.begin() as connection:
        result = connection.execute(stmt)

    inserted = result.rowcount
    total = len(records)
    skipped = total - inserted

    if inserted == 0:
        logger.info("No new records inserted. All data already exists.")
    else:
        logger.info(
            f"Inserted {inserted} records, skipped {skipped} duplicates."
        )
