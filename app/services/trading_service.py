
import asyncio
import pandas as pd
from sqlalchemy.orm import Session
from app.config import settings
from app.exchange.binance_public import BinanceMarketData
from app.strategies.ema_crossover import generate_signal
from app.simulator.paper_broker import ensure_account, market_buy, market_sell, reset_account as paper_reset
from app.models import Trade, Position

async def fetch_candles(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    md = BinanceMarketData(settings.BINANCE_BASE_URL)
    return await md.get_klines_async(symbol, interval, limit)

def run_strategy_once(session: Session):
    # 1) Pull candles
    df = asyncio.run(fetch_candles(settings.SYMBOL, settings.INTERVAL, settings.LOOKBACK))
    last_close = float(df["close"].iloc[-1])

    # 2) Determine signal
    signal = generate_signal(df, settings.FAST_EMA, settings.SLOW_EMA)

    # 3) Get/current paper pos
    pos = ensure_account(session, settings.SYMBOL)

    order_result = None
    if signal == "BUY" and pos.quote_qty > settings.POSITION_SIZE_USDT:
        order_result = market_buy(session, settings.SYMBOL, last_close, settings.POSITION_SIZE_USDT)
    elif signal == "SELL" and pos.base_qty > 0:
        order_result = market_sell(session, settings.SYMBOL, last_close, pos.base_qty)
    else:
        # HOLD or insufficient balance
        pass

    return {
        "symbol": settings.SYMBOL,
        "interval": settings.INTERVAL,
        "signal": signal,
        "last_close": last_close,
        "position": {"base_qty": pos.base_qty, "quote_qty": pos.quote_qty},
        "order_executed": bool(order_result),
        "order": {
            "side": getattr(order_result, "side", None),
            "qty": getattr(order_result, "qty", None),
            "price": getattr(order_result, "price", None),
        } if order_result else None
    }

def list_trades(session: Session):
    q = session.query(Trade).order_by(Trade.id.desc()).all()
    return [
        {
            "id": t.id,
            "symbol": t.symbol,
            "side": t.side,
            "qty": t.qty,
            "price": t.price,
            "fee": t.fee,
            "is_live": t.is_live,
            "created_at": t.created_at.isoformat() + "Z"
        } for t in q
    ]

def reset_paper_account(session: Session):
    paper_reset(session, settings.SYMBOL)
