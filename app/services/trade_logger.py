def log_trade_open(ticket, symbol, type_, volume, price):
    from app.db.session import SessionLocal
    from app.repositories.trades import TradeCreate, TradeRepository

    db = SessionLocal()
    try:
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
    finally:
        db.close()


def update_trade_close(ticket, close_price, profit):
    from app.db.session import SessionLocal
    from app.repositories.trades import TradeRepository

    db = SessionLocal()
    try:
        repo = TradeRepository(db)
        repo.mark_closed(
            ticket=int(ticket),
            close_price=float(close_price),
            profit=float(profit),
        )
    finally:
        db.close()


def get_trades():
    from app.db.session import SessionLocal
    from app.repositories.trades import TradeRepository

    db = SessionLocal()
    try:
        repo = TradeRepository(db)
        return repo.list_recent()
    finally:
        db.close()
