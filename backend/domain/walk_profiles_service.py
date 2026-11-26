from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.entrances_model import entrances
from domain.walk_profiles_model import walk_profiles
from domain.detours_model import detours
from domain.map_notes_model import map_notes


def draft_profile(conn, user, data):
    need(isinstance(data.avoid, list) and data.avoid and all(isinstance(x,str) and x for x in data.avoid),
         '至少提供一个有效避让标记')
    need(isinstance(data.weights, dict), '权重应为对象')
    need(set(data.weights) == set(data.avoid) and all(type(x) in (int,float) and 0 < x <= 5 for x in data.weights.values()),
         '每条应规避标记须有 0 至 5 的权重')
    need(0 <= data.minimum <= 1, '匹配分门槛必须在 0 到 1')
    need(any(row['park'] == data.park for row in scan(conn, entrances)), '公园尚未登记入口')
    return insert(conn, walk_profiles, **data.model_dump())


def match_entrances(conn, user, data):
    profile = get(conn, walk_profiles, data.profile)
    observed = [row for row in scan(conn, entrances) if row['park'] == profile['park']
                and row['condition'] == '现场见证']
    need(observed, '没有见证过的入口')
    return submit(user, {'profile':profile,'entrances':observed})
