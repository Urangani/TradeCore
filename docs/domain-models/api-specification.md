# API Specification

This document defines the REST and WebSocket interfaces for the TradeCore FastAPI backend.

## 🌐 REST API Endpoints

### 1. Strategy Management
- `GET /strategies`: List all strategies.
- `POST /strategies`: Register a new strategy.
- `GET /strategies/{id}`: Get details of a specific strategy.
- `PATCH /strategies/{id}`: Update parameters or toggle `is_active`.

### 2. Signal & Execution
- `GET /signals`: List signal history.
- `POST /signals`: MT5/Python listener posts a new signal.
- `GET /signals/{id}`: Get details of a specific signal.

### 3. Trade & Order History
- `GET /trades`: List all closed trades.
- `GET /orders`: List all active/pending orders.
- `GET /trades/{id}`: Get specific trade details.

### 4. System Status
- `GET /health`: Check backend and DB status.
- `GET /account`: Get current account state (balance, equity).

---

## ⚡ WebSocket Endpoints

### 1. `/ws/ticks`
Broadcasting real-time market data to dashboards.
- **Message Format (JSON)**:
  ```json
  {
    "type": "tick",
    "symbol": "EURUSD",
    "bid": 1.0850,
    "ask": 1.0852,
    "timestamp": "2026-04-30T12:00:00Z"
  }
  ```

### 2. `/ws/signals`
Real-time signal notifications.
- **Message Format (JSON)**:
  ```json
  {
    "type": "signal",
    "strategy_id": "uuid-123",
    "symbol": "GBPUSD",
    "direction": "BUY",
    "price": 1.2540,
    "timestamp": "2026-04-30T12:05:00Z"
  }
  ```

### 3. `/ws/status`
System-wide health and account updates.
- **Message Format (JSON)**:
  ```json
  {
    "type": "account_update",
    "equity": 10500.50,
    "margin_level": 500.0
  }
  ```

---

## 🔐 Security
- **Authentication**: JWT (JSON Web Tokens) for dashboard users.
- **API Keys**: Shared secret for the MT5 Ingestion Layer -> FastAPI communication.

