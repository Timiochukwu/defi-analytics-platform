"""
Application settings and configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # Application
    APP_NAME: str = "DeFi Analytics Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    API_WORKERS: int = 4

    # Security
    API_SECRET_KEY: str = "your-secret-key-change-in-production"
    API_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Web3
    ETHEREUM_RPC_URL: str = "http://localhost:8545"
    CHAIN_ID: int = 1

    # The Graph
    THE_GRAPH_API_KEY: Optional[str] = None
    UNISWAP_GRAPH_URL: str = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
    AAVE_GRAPH_URL: str = "https://api.thegraph.com/subgraphs/name/aave/protocol-v3"

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/defi_analytics"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL: int = 3600

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "color"
    LOG_FILE_PATH: str = "logs/defi_analytics.log"

    # External APIs
    COINGECKO_API_KEY: Optional[str] = None
    COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"
    ETHERSCAN_API_KEY: Optional[str] = None
    DEFILLAMA_API_URL: str = "https://api.llama.fi"

    # Data Collection
    DATA_REFRESH_INTERVAL: int = 300  # seconds
    ENABLE_BACKGROUND_TASKS: bool = True

    # Risk Parameters
    DEFAULT_RISK_TOLERANCE: float = 3.0
    MIN_PROTOCOL_AGE_DAYS: int = 30
    MIN_AUDIT_SCORE: float = 70.0

    # Portfolio Optimization
    MAX_POSITION_SIZE: float = 0.40
    MIN_LIQUIDITY_USD: float = 1_000_000

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance

    Returns:
        Settings instance
    """
    return Settings()
