from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


walk_profiles = Table('walk_profiles', metadata,
    Column('code', String(64), primary_key=True),
    Column('park', String(160), nullable=False),
    Column('avoid', JSON, nullable=False),
    Column('weights', JSON, nullable=False),
    Column('minimum', Float, nullable=False),
    CheckConstraint('minimum between 0 and 1'),
)
