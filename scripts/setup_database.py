"""
Database setup script
Run this to initialize the database schema
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.config import get_settings


def setup_database():
    """Initialize database schema"""
    settings = get_settings()

    print("Setting up database...")
    print(f"Database URL: {settings.DATABASE_URL}")

    try:
        engine = create_engine(settings.DATABASE_URL)

        with engine.connect() as conn:
            # Create tables (extend this with actual schema)
            print("Creating tables...")

            # Example: Create protocols table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS protocols (
                    id SERIAL PRIMARY KEY,
                    protocol_id VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    protocol_type VARCHAR(100) NOT NULL,
                    chain VARCHAR(50) NOT NULL,
                    tvl_usd DECIMAL(20, 2),
                    contract_address VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            # Example: Create portfolios table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS portfolios (
                    id SERIAL PRIMARY KEY,
                    portfolio_id VARCHAR(255) UNIQUE NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    strategy VARCHAR(50) NOT NULL,
                    initial_capital_usd DECIMAL(20, 2),
                    current_value_usd DECIMAL(20, 2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            # Example: Create positions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS positions (
                    id SERIAL PRIMARY KEY,
                    position_id VARCHAR(255) UNIQUE NOT NULL,
                    portfolio_id VARCHAR(255) REFERENCES portfolios(portfolio_id),
                    protocol_name VARCHAR(255) NOT NULL,
                    position_type VARCHAR(50) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    asset_symbol VARCHAR(50) NOT NULL,
                    amount DECIMAL(30, 18),
                    value_usd DECIMAL(20, 2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            conn.commit()

        print("✓ Database setup complete!")

    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_database()
