"""Initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-30 15:45:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    signal_direction = sa.Enum("BUY", "SELL", "EXIT", name="signaldirection")
    order_status = sa.Enum("PENDING", "OPEN", "CANCELLED", name="orderstatus")

    bind = op.get_bind()
    if bind.dialect.name != "sqlite":
        signal_direction.create(bind, checkfirst=True)
        order_status.create(bind, checkfirst=True)

    op.create_table(
        "account_state",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Float(), nullable=False),
        sa.Column("equity", sa.Float(), nullable=False),
        sa.Column("margin", sa.Float(), nullable=False),
        sa.Column("free_margin", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_account_state_timestamp"), "account_state", ["timestamp"], unique=False)

    op.create_table(
        "strategies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("params", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_strategies_name"), "strategies", ["name"], unique=True)

    op.create_table(
        "ticks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("bid", sa.Float(), nullable=False),
        sa.Column("ask", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ticks_symbol"), "ticks", ["symbol"], unique=False)
    op.create_index(op.f("ix_ticks_timestamp"), "ticks", ["timestamp"], unique=False)

    op.create_table(
        "signals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("strategy_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("signal", signal_direction, nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["strategy_id"], ["strategies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_signals_strategy_id"), "signals", ["strategy_id"], unique=False)
    op.create_index(op.f("ix_signals_symbol"), "signals", ["symbol"], unique=False)

    op.create_table(
        "orders",
        sa.Column("ticket", sa.Integer(), nullable=False),
        sa.Column("signal_id", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.Column("open_price", sa.Float(), nullable=False),
        sa.Column("status", order_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["signal_id"], ["signals.id"]),
        sa.PrimaryKeyConstraint("ticket"),
    )
    op.create_index(op.f("ix_orders_signal_id"), "orders", ["signal_id"], unique=False)
    op.create_index(op.f("ix_orders_symbol"), "orders", ["symbol"], unique=False)

    op.create_table(
        "trades",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("strategy_id", sa.Integer(), nullable=False),
        sa.Column("signal_id", sa.Integer(), nullable=True),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("close_price", sa.Float(), nullable=True),
        sa.Column("profit", sa.Float(), nullable=True),
        sa.Column("swap", sa.Float(), nullable=True),
        sa.Column("commission", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["signal_id"], ["signals.id"]),
        sa.ForeignKeyConstraint(["strategy_id"], ["strategies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_trades_signal_id"), "trades", ["signal_id"], unique=False)
    op.create_index(op.f("ix_trades_strategy_id"), "trades", ["strategy_id"], unique=False)
    op.create_index(op.f("ix_trades_symbol"), "trades", ["symbol"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_trades_symbol"), table_name="trades")
    op.drop_index(op.f("ix_trades_strategy_id"), table_name="trades")
    op.drop_index(op.f("ix_trades_signal_id"), table_name="trades")
    op.drop_table("trades")

    op.drop_index(op.f("ix_orders_symbol"), table_name="orders")
    op.drop_index(op.f("ix_orders_signal_id"), table_name="orders")
    op.drop_table("orders")

    op.drop_index(op.f("ix_signals_symbol"), table_name="signals")
    op.drop_index(op.f("ix_signals_strategy_id"), table_name="signals")
    op.drop_table("signals")

    op.drop_index(op.f("ix_ticks_timestamp"), table_name="ticks")
    op.drop_index(op.f("ix_ticks_symbol"), table_name="ticks")
    op.drop_table("ticks")

    op.drop_index(op.f("ix_strategies_name"), table_name="strategies")
    op.drop_table("strategies")

    op.drop_index(op.f("ix_account_state_timestamp"), table_name="account_state")
    op.drop_table("account_state")

    bind = op.get_bind()
    if bind.dialect.name != "sqlite":
        sa.Enum(name="orderstatus").drop(bind, checkfirst=True)
        sa.Enum(name="signaldirection").drop(bind, checkfirst=True)
