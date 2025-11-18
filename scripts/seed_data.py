"""
Seed database with sample data for testing
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import uuid

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from src.config import get_settings


def seed_protocols(conn):
    """Seed sample protocols"""
    protocols = [
        {
            'protocol_id': str(uuid.uuid4()),
            'name': 'Aave',
            'protocol_type': 'lending',
            'chain': 'ethereum',
            'tvl_usd': 5000000000,
            'contract_address': '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'
        },
        {
            'protocol_id': str(uuid.uuid4()),
            'name': 'Uniswap V3',
            'protocol_type': 'dex',
            'chain': 'ethereum',
            'tvl_usd': 3500000000,
            'contract_address': '0x1F98431c8aD98523631AE4a59f267346ea31F984'
        },
        {
            'protocol_id': str(uuid.uuid4()),
            'name': 'Compound',
            'protocol_type': 'lending',
            'chain': 'ethereum',
            'tvl_usd': 2800000000,
            'contract_address': '0xc00e94Cb662C3520282E6f5717214004A7f26888'
        },
    ]

    for protocol in protocols:
        conn.execute(text("""
            INSERT INTO protocols (protocol_id, name, protocol_type, chain, tvl_usd, contract_address)
            VALUES (:protocol_id, :name, :protocol_type, :chain, :tvl_usd, :contract_address)
            ON CONFLICT (protocol_id) DO NOTHING
        """), protocol)

    print(f"✓ Seeded {len(protocols)} protocols")


def seed_data():
    """Seed all sample data"""
    settings = get_settings()

    print("Seeding database with sample data...")

    try:
        engine = create_engine(settings.DATABASE_URL)

        with engine.connect() as conn:
            seed_protocols(conn)
            conn.commit()

        print("✓ Database seeding complete!")

    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    seed_data()
