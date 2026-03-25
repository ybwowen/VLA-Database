import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def build_database_url():
    raw_url = os.getenv("DATABASE_URL")
    if raw_url:
        return raw_url

    user = os.getenv("MYSQL_USER", "vla_user")
    password = quote_plus(os.getenv("MYSQL_PASSWORD", "change_me"))
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE", "vla_database")
    return (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/"
        f"{database}?charset=utf8mb4"
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "vla-course-project")
    DATABASE_URL = build_database_url()
