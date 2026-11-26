from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


entrances = Table('entrances', metadata,
    Column('code', String(64), primary_key=True),
    Column('park', String(160), nullable=False),
    Column('ramp', Boolean, nullable=False),
    Column('tags', JSON, nullable=False),
    Column('condition', String(160), nullable=False),
)
