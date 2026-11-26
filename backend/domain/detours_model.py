from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


detours = Table('detours', metadata,
    Column('code', String(64), primary_key=True),
    Column('profile', String(160), ForeignKey('walk_profiles.code'), nullable=False),
    Column('entrance', String(160), ForeignKey('entrances.code'), nullable=False),
    Column('walk_m', Integer, nullable=False),
    Column('score', Float, nullable=False),
    Column('state', String(160), nullable=False),
    CheckConstraint('walk_m between 1 and 3000'),
    CheckConstraint('score between 0 and 1'),
)
