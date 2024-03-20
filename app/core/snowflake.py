from app.core.config import settings
from snowflake import SnowflakeGenerator


def generate_snowflake_id():
    gen = SnowflakeGenerator(settings.WORKER_ID, seq=settings.WORKER_SEQ)
    return next(gen)
