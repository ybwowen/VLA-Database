import re

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


Base = declarative_base()
SessionLocal = scoped_session(
    sessionmaker(autoflush=False, autocommit=False, expire_on_commit=False)
)
_engine = None


def init_engine(database_url):
    global _engine

    if _engine is not None and str(_engine.url) == database_url:
        return _engine

    _engine = create_engine(
        database_url,
        future=True,
        pool_pre_ping=True,
        pool_recycle=280,
    )
    SessionLocal.remove()
    SessionLocal.configure(bind=_engine)
    return _engine


def get_engine():
    if _engine is None:
        raise RuntimeError("Database engine has not been initialized.")
    return _engine


def get_session():
    return SessionLocal()


def remove_session(exception=None):
    SessionLocal.remove()


def ensure_database_exists(database_url):
    url = make_url(database_url)
    database_name = url.database

    if url.get_backend_name() != "mysql":
        raise ValueError("This project expects a MySQL database URL.")

    if not database_name or not re.fullmatch(r"[A-Za-z0-9_]+", database_name):
        raise ValueError("MYSQL_DATABASE must contain only letters, digits, and underscores.")

    admin_url = url.set(database=None)
    admin_engine = create_engine(admin_url, future=True, pool_pre_ping=True)

    try:
        with admin_engine.connect() as connection:
            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
            connection.commit()
    finally:
        admin_engine.dispose()
