from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo

class Settings(BaseSettings):
    SYMBOL: str = "BTCUSDT"
    INTERVAL: str = "1m"
    LOOKBACK: int = 300

    PAPER_STARTING_USDT: float = 10000.0
    PAPER_FEE_RATE: float = 0.001
    PAPER_SLIPPAGE_BPS: float = 5.0

    FAST_EMA: int = 9
    SLOW_EMA: int = 21
    POSITION_SIZE_USDT: float = 250.0

    LIVE_TRADING: bool = False
    BINANCE_API_KEY: str | None = None
    BINANCE_API_SECRET: str | None = None
    BINANCE_BASE_URL: str = "https://api.binance.com"  # For Binance.US: https://api.binance.us

    DB_URL: str = "sqlite:///./trades.db"

    @field_validator("SLOW_EMA")
    @classmethod
    def validate_emas(cls, v: int, info: ValidationInfo) -> int:
        fast = info.data.get("FAST_EMA", 9)
        if v <= fast:
            raise ValueError("SLOW_EMA must be greater than FAST_EMA")
        return v

settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
