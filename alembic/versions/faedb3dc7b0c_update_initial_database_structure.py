"""update initial database structure

Revision ID: faedb3dc7b0c
Revises: 04854ae183a0
Create Date: 2025-03-20 18:20:42.166546

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "faedb3dc7b0c"
down_revision: Union[str, None] = "04854ae183a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_chat",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"], ["chats.id"], name="fk_user_chat_chat_id", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="fk_user_chat_user_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("user_id", "chat_id"),
    )
    op.add_column("chats", sa.Column("api_key", sa.String(), nullable=True))
    op.add_column(
        "chats",
        sa.Column(
            "tts_model",
            sa.String(),
            server_default="TeraTTS/glados2-g2p-vits",
            nullable=False,
        ),
    )
    op.add_column(
        "chats",
        sa.Column(
            "history_depth", sa.BigInteger(), server_default="1000", nullable=False
        ),
    )
    op.add_column(
        "chats",
        sa.Column("tts_length_scale", sa.Float(), server_default="1.2", nullable=False),
    )
    op.add_column(
        "chats",
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.add_column("messages", sa.Column("user_id", sa.BigInteger(), nullable=False))
    op.add_column(
        "messages",
        sa.Column(
            "generation_time_ms", sa.Float(), server_default="0.0", nullable=False
        ),
    )
    op.add_column(
        "messages",
        sa.Column(
            "history_part",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.add_column(
        "messages",
        sa.Column(
            "from_bot", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
    )
    op.add_column(
        "messages",
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.create_foreign_key(
        "fk_message_user_id",
        "messages",
        "users",
        ["user_id"],
        ["id"],
        ondelete="NO ACTION",
    )
    op.add_column(
        "users",
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.alter_column(
        "users",
        "reputation",
        existing_type=sa.BIGINT(),
        type_=sa.Float(),
        existing_nullable=False,
        existing_server_default=sa.text("'0'::bigint"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "reputation",
        existing_type=sa.Float(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        existing_server_default=sa.text("'0'::bigint"),
    )
    op.drop_column("users", "timestamp")

    op.drop_constraint("fk_message_user_id", "messages", type_="foreignkey")
    op.drop_column("messages", "timestamp")
    op.drop_column("messages", "from_bot")
    op.drop_column("messages", "history_part")
    op.drop_column("messages", "generation_time_ms")
    op.drop_column("messages", "user_id")
    op.drop_column("chats", "timestamp")
    op.drop_column("chats", "tts_length_scale")
    op.drop_column("chats", "history_depth")
    op.drop_column("chats", "tts_model")
    op.drop_column("chats", "api_key")
    op.drop_table("user_chat")
    # ### end Alembic commands ###
