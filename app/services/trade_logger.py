from sqlalchemy.orm import Session
from app.repositories.trades import TradeCreate, TradeRepository

def log_trade_open(db: Session, ticket, symbol, type_, volume, price):
    repo = TradeRepository(db)
    repo.create_open(
        TradeCreate(
            ticket=int(ticket),
            symbol=symbol,
            side=type_,
            volume=float(volume),
            open_price=float(price) if price is not None else None,
        )
    )

def update_trade_close(db: Session, ticket, close_price, profit):
    repo = TradeRepository(db)
    repo.mark_closed(
        ticket=int(ticket),
        close_price=float(close_price),
        profit=float(profit),
    )

def get_trades(db: Session):
    repo = TradeRepository(db)
    return repo.list_recent()
