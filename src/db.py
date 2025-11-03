from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Text,
    func,
    text,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# JSONB-backed table matching migration: pessoas(id UUID PK, data JSONB, created_at)
class PessoaJSON(Base):
    __tablename__ = "pessoas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = Column(JSONB, nullable=False)  # stores full PessoaFisica JSON
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    def __repr__(self):
        return f"<PessoaJSON id={self.id} created_at={self.created_at}>"

# Optionally: helper to create tables (sync) for quick local dev
def create_all(engine):
    """
    Create all tables in DB. For async setups, use metadata.create_all in a sync engine or use Alembic for production.
    """
    Base.metadata.create_all(bind=engine)