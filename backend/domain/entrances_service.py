from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.entrances_model import entrances
from domain.walk_profiles_model import walk_profiles
from domain.detours_model import detours
from domain.map_notes_model import map_notes


def inspect(conn, user, data):
    get(conn, entrances, data.entrance, lock=True)
    return update(conn, entrances, data.entrance, ramp=data.ramp, condition='现场见证')
