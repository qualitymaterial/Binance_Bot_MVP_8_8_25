
from sqlalchemy.orm import Session
from app.models import Trade, Position
from app.config import settings

FEE_RATE = settings.PAPER_FEE_RATE
SLIPPAGE = settings.PAPER_SLIPPAGE_BPS / 10000.0

def ensure_account(session: Session, symbol: str):
    pos = session.query(Position).filter_by(symbol=symbol).first()
    if not pos:
        pos = Position(symbol=symbol, base_qty=0.0, quote_qty=settings.PAPER_STARTING_USDT)
        session.add(pos)
        session.commit()
    return pos

def market_buy(session: Session, symbol: str, price: float, quote_amount: float):
    price = price * (1 + SLIPPAGE)
    qty = quote_amount / price
    fee = quote_amount * FEE_RATE
    pos = ensure_account(session, symbol)
    if pos.quote_qty < quote_amount + fee:
        raise ValueError("Insufficient quote (USDT) for paper BUY")
    pos.quote_qty -= (quote_amount + fee)
    pos.base_qty += qty
    trade = Trade(symbol=symbol, side="BUY", qty=qty, price=price, fee=fee, is_live=False)
    session.add(trade)
    session.commit()
    return trade

def market_sell(session: Session, symbol: str, price: float, base_qty: float):
    price = price * (1 - SLIPPAGE)
    proceeds = base_qty * price
    fee = proceeds * FEE_RATE
    pos = ensure_account(session, symbol)
    if pos.base_qty < base_qty:
        raise ValueError("Insufficient base asset for paper SELL")
    pos.base_qty -= base_qty
    pos.quote_qty += (proceeds - fee)
    trade = Trade(symbol=symbol, side="SELL", qty=base_qty, price=price, fee=fee, is_live=False)
    session.add(trade)
    session.commit()
    return trade

def reset_account(session: Session, symbol: str):
    pos = session.query(Position).filter_by(symbol=symbol).first()
    if not pos:
        pos = Position(symbol=symbol, base_qty=0.0, quote_qty=settings.PAPER_STARTING_USDT)
        session.add(pos)
    else:
        pos.base_qty = 0.0
        pos.quote_qty = settings.PAPER_STARTING_USDT
    session.query(Trade).filter_by(symbol=symbol).delete()
    session.commit()
