import enum
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ActivityLevel(str, enum.Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    very_active = "very_active"


class Goal(str, enum.Enum):
    lose_weight = "lose_weight"
    maintain = "maintain"
    gain_weight = "gain_weight"
    manage_condition = "manage_condition"


class MealSource(str, enum.Enum):
    chat = "chat"
    photo = "photo"
    manual = "manual"


class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"
    tool = "tool"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)
    age: Mapped[int | None] = mapped_column(nullable=True)
    sex: Mapped[str | None] = mapped_column(String(10), nullable=True)
    height_cm: Mapped[float | None] = mapped_column(
        Numeric(5, 1), nullable=True
    )
    weight_kg: Mapped[float | None] = mapped_column(
        Numeric(5, 1), nullable=True
    )
    activity_level: Mapped[ActivityLevel] = mapped_column(
        Enum(ActivityLevel, name="activity_level"),
        default=ActivityLevel.moderate,
    )
    conditions: Mapped[list[str]] = mapped_column(JSON, default=list)
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list)
    goal: Mapped[Goal] = mapped_column(
        Enum(Goal, name="goal"), default=Goal.maintain
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default="now()"
    )


class FoodItem(Base):
    __tablename__ = "food_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name_en: Mapped[str] = mapped_column(String(120))
    name_sw: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(60))
    serving_size_g: Mapped[float] = mapped_column(Numeric(6, 1))
    calories_kcal: Mapped[float] = mapped_column(Numeric(6, 1))
    protein_g: Mapped[float] = mapped_column(Numeric(5, 1))
    carbs_g: Mapped[float] = mapped_column(Numeric(5, 1))
    fat_g: Mapped[float] = mapped_column(Numeric(5, 1))
    fiber_g: Mapped[float] = mapped_column(Numeric(5, 1))
    key_micronutrients: Mapped[dict] = mapped_column(JSON, default=dict)
    common_allergens: Mapped[list[str]] = mapped_column(JSON, default=list)
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(768), nullable=True
    )


class MealLog(Base):
    __tablename__ = "meal_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    food_items: Mapped[list[dict]] = mapped_column(JSON, default=list)
    logged_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default="now()"
    )
    source: Mapped[MealSource] = mapped_column(
        Enum(MealSource, name="meal_source")
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default="now()"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id")
    )
    role: Mapped[MessageRole] = mapped_column(
        Enum(MessageRole, name="message_role")
    )
    content: Mapped[str] = mapped_column(Text)
    tool_calls: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default="now()"
    )
    conversation: Mapped[Conversation] = relationship(
        back_populates="messages"
    )