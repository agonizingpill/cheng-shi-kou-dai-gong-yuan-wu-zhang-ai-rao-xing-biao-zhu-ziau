from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.entrances_model import entrances
from domain.walk_profiles_model import walk_profiles
from domain.detours_model import detours
from domain.map_notes_model import map_notes


def publish_map(conn, user, data):
    route = get(conn, detours, data.detour, lock=True)
    need(route['state'] == '待地图签注', '该提报已闭合或退回')
    entrance = get(conn, entrances, route['entrance'], lock=True)
    accessible = entrance['ramp'] and entrance['condition'] == '现场见证'
    legend = (f"经 {entrance['code']} 坡道步行 {route['walk_m']} 米" if accessible
              else '替代坡道不可用，绕行受阻，请查看现场导视')
    output = insert(conn, map_notes, **data.model_dump(), legend=legend)
    update(conn, detours, data.detour, state='地图已签注' if accessible else '仅告知受阻')
    return output
