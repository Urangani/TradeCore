# Database Schema Design

This document defines the data structures for the TradeCore system. It is designed to be compatible with SQLAlchemy (for Python integration) and supports the transition from SQLite (Dev) to PostgreSQL (Prod).

## 📊 Entity Relationship Summary

The system tracks MT5 market activity, Python-generated signals, and the link between them (strategies).

### 1. `strategies`
Metadata for trading algorithms.
| Column | Type | Description |
| --- | --- | --- |
| `id` | UUID/Integer | Primary Key |
| `name` | String | Unique name of the strategy |
| `version` | String | Version tracking |
| `params` | JSON | Parameter configuration (e.g., SL/TP settings) |
| `is_active` | Boolean | Whether the strategy is live |
| `created_at` | DateTime | Timestamp |

### 2. `ticks` (Market Data)
High-frequency market prID | Primary Key |
| `strategy_id` | FK(strategies) | Link to the strategy |
| `symbol` | String | Asset symbol |
| `direction` | Enum | BUY, SELL, EXIT |
| `price` | Float | Signal price |
| `timestamp` | DateTime | Generation time |

### 4. `orders`
Active or pending instructions in MT5.
| Column | Type | Description |
| --- | --- | --- |
| `ticket` | BigInt | MT5 Ticket Number (Primary Key) |
| `signal_id` | FK(signals) | Link to the triggering signal |
| `symbol` | String | Asset symbol |
| `type` | Enum | BUY, SELL, etc. |
| `volume` | Float | Lot size |
| `open_price` | Float | Price at entry |
| `status` | Enum | PENDING, OPEN, CANCELLED |ice updates.
| Column | Type | Description |
| --- | --- | --- |
| `id` | BigInt | Primary Key |
| `symbol` | String | e.g., "EURUSD" |
| `bid` | Float | Bid price |
| `ask` | Float | Ask price |
| `timestamp` | DateTime | Precise tick time |

### 3. `signals`
Logic outputs from the Strategy Engine.
| Column | Type | Description |
| --- | --- | --- |
| `id` | UU
| `created_at` | DateTime | Timestamp |

### 5. `trades`
Closed positions (Historical data).
| Column | Type | Description |
| --- | --- | --- |
| `id` | UUID | Primary Key |
| `ticket` | BigInt | MT5 Ticket Number |
| `signal_id` | FK(signals) | Link to the signal |
| `profit` | Float | Realized profit/loss |
| `swap` | Float | Swap costs |
| `commission` | Float | Broker commission |
| `close_price` | Float | Price at exit |
| `close_time` | DateTime | Exit timestamp |

### 6. `account_state`
Snapshot of account health.
| Column | Type | Description |
| --- | --- | --- |
| `id` | Integer | Primary Key |
| `balance` | Float | Current balance |
| `equity` | Float | Current equity |
| `margin` | Float | Used margin |
| `free_margin` | Float | Available margin |
| `timestamp` | DateTime | Snapshot time |

---

## 🚀 Migration Strategy
- **Phase 1**: Initial implementation using **SQLite** for rapid local development.
- **Phase 2**: Use **Alembic** to manage schema versions.
- **Phase 3**: Migrate to **PostgreSQL** by updating the SQLAlchemy connection string; Alembic handles the DDL differences.
