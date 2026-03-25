import argparse
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app import create_app
from app.db import Base, ensure_database_exists, get_engine, get_session, remove_session
from app.seed_data import load_seed_data


def main():
    parser = argparse.ArgumentParser(description="Initialize the MySQL schema and load seed data.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all tables before recreating them and reloading seed data.",
    )
    args = parser.parse_args()

    app = create_app()
    database_url = app.config["DATABASE_URL"]

    try:
        ensure_database_exists(database_url)
        engine = get_engine()

        if args.reset:
            Base.metadata.drop_all(bind=engine)

        Base.metadata.create_all(bind=engine)

        session = get_session()
        try:
            result = load_seed_data(session)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            remove_session()

        print(result["message"])
    except SQLAlchemyError as exc:
        print("Database initialization failed.")
        print("Check your MySQL server, account, and .env configuration.")
        print(f"SQLAlchemy error: {exc}")
        raise SystemExit(1)
    except Exception as exc:
        print(f"Initialization failed: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
