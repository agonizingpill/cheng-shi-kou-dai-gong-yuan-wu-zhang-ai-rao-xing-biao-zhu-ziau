from domain.entrances_model import entrances
from domain.walk_profiles_model import walk_profiles
from domain.detours_model import detours
from domain.map_notes_model import map_notes

FIXTURES = [
    (entrances, [{'code': 'PK-E1',
  'park': '柳瓦园',
  'ramp': False,
  'tags': ['石阶', '碎石'],
  'condition': '现场见证'},
 {'code': 'PK-E2', 'park': '柳瓦园', 'ramp': True, 'tags': ['临时标线'], 'condition': '现场见证'},
 {'code': 'PK-E3',
  'park': '柳瓦园',
  'ramp': True,
  'tags': ['石阶', '碎石'],
  'condition': '现场见证'},
 {'code': 'PK-W1', 'park': '银叶园', 'ramp': True, 'tags': ['木栈道'], 'condition': '暂闭'}]),
    (walk_profiles, [{'code': 'PR-10',
  'park': '柳瓦园',
  'avoid': ['石阶', '碎石'],
  'weights': {'石阶': 2, '碎石': 1},
  'minimum': 0.7}]),
    (detours, [{'code': 'DP-01',
  'profile': 'PR-10',
  'entrance': 'PK-E2',
  'walk_m': 72,
  'score': 1,
  'state': '地图已签注'}]),
    (map_notes, [{'code': 'NOTE-10',
  'detour': 'DP-01',
  'legend': '从东侧坡道绕行约 72 米',
  'edition': '2026-11-24a'}]),
]
