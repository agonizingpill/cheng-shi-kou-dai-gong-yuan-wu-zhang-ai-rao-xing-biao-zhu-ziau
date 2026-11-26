from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.entrances_model import entrances
from domain.walk_profiles_model import walk_profiles
from domain.detours_model import detours
from domain.map_notes_model import map_notes


def submit_detour(conn, user, data):
    run = result(user, data.token)
    profile = run['input']['profile']
    entrance = get(conn, entrances, data.entrance, lock=True)
    candidate = next((item for item in run['result']['ranked'] if item['entry']==data.entrance),None)
    need(candidate and entrance['park'] == profile['park'], '入口不属于这张偏好卡')
    need(candidate['score'] >= profile['minimum'], '障碍组合匹配分不足')
    need(1 <= data.walk_m <= 3000, '步测长度超出地图标注范围')
    return insert(conn, detours, code=data.code, profile=profile['code'], entrance=data.entrance,
                  walk_m=data.walk_m, score=candidate['score'], state='待地图签注')


def withdraw_detour(conn, user, data):
    record = get(conn, detours, data.detour, lock=True)
    need(record['state'] == '待地图签注', '已签注线路须另建改版单')
    return update(conn, detours, data.detour, state='退回 '+data.reason)
