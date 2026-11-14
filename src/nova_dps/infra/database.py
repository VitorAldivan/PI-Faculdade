import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///nova_dps.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
