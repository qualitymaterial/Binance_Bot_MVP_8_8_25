
from fastapi import FastAPI, Depends
from app.models import Base, engine, get_session
from sqlalchemy.orm import Session
from app.services.trading_service import run_strategy_once, reset_paper_account, list_trades

app = FastAPI(title="Binance Trading Bot — MVP", version="0.1.0")

# Create tables on startup
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/strategy/run")
def strategy_run(session: Session = Depends(get_session)):
    result = run_strategy_once(session)
    return result

@app.get("/trades")
def trades(session: Session = Depends(get_session)):
    return list_trades(session)

@app.post("/paper/reset")
def paper_reset(session: Session = Depends(get_session)):
    reset_paper_account(session)
    return {"message": "Paper account reset."}
