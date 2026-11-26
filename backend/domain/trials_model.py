from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


weight_trials = Table('weight_trials', metadata,
    Column('code', String(64), primary_key=True),
    Column('profile', String(160), ForeignKey('walk_profiles.code'), nullable=False),
    Column('weights_b', JSON, nullable=False),
    Column('threshold', Float, nullable=False),
    Column('state', String(160), nullable=False),
    CheckConstraint('threshold between 0 and 1'),
)

trial_entries = Table('trial_entries', metadata,
    Column('trial', String(160), ForeignKey('weight_trials.code'), primary_key=True),
    Column('entrance', String(160), ForeignKey('entrances.code'), primary_key=True),
    Column('tags', JSON, nullable=False),
    Column('judgment', String(160), nullable=True),
    Column('score_a', Float, nullable=True),
    Column('score_b', Float, nullable=True),
)

trial_conclusions = Table('trial_conclusions', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('trial', String(160), ForeignKey('weight_trials.code'), nullable=False),
    Column('false_pass_a', Integer, nullable=False),
    Column('false_pass_b', Integer, nullable=False),
    Column('verdict', String(160), nullable=False),
    Column('cause', String(160), nullable=False),
    Column('at', DateTime, nullable=False),
)
