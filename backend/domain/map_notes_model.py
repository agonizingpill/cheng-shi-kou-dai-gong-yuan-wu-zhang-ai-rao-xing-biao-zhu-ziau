from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


map_notes = Table('map_notes', metadata,
    Column('code', String(64), primary_key=True),
    Column('detour', String(160), ForeignKey('detours.code'), nullable=False, unique=True),
    Column('legend', String(160), nullable=False),
    Column('edition', String(160), nullable=False, unique=True),
)
