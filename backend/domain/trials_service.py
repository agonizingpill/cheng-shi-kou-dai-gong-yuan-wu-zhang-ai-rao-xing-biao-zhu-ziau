from sqlalchemy import select

from core.queueing import submit
from core.records import get, insert, need, scan
from domain.entrances_model import entrances
from domain.trials_model import trial_conclusions, trial_entries, weight_trials
from domain.trials_scoring import entries_of, false_passed, latest_conclusion, settle
from domain.walk_profiles_model import walk_profiles


def list_trials(conn):
    rows = scan(conn, weight_trials)
    for row in rows:
        latest = latest_conclusion(conn, row['code'])
        row['false_pass_a'] = latest['false_pass_a'] if latest else None
        row['false_pass_b'] = latest['false_pass_b'] if latest else None
        row['verdict'] = latest['verdict'] if latest else None
    return rows


def draft_trial(conn, user, data):
    profile = get(conn, walk_profiles, data.profile)
    need(isinstance(data.weights_b, dict), '候选权重应为对象')
    need(set(data.weights_b) == set(profile['avoid'])
         and all(type(x) in (int, float) and 0 < x <= 5 for x in data.weights_b.values()),
         '候选权重须与偏好卡避让标记一一对应，取值 0 至 5')
    need(0 <= data.threshold <= 1, '放行门槛必须在 0 到 1')
    batch = [row for row in scan(conn, entrances)
             if row['park'] == profile['park'] and row['condition'] == '现场见证']
    need(batch, '没有见证过的入口')
    insert(conn, weight_trials, code=data.code, profile=profile['code'],
           weights_b=data.weights_b, threshold=data.threshold, state='试算中')
    for row in batch:
        conn.execute(trial_entries.insert().values(trial=data.code, entrance=row['code'],
                                                   tags=row['tags'], judgment=None,
                                                   score_a=None, score_b=None))
    return get(conn, weight_trials, data.code)


def judge_entry(conn, user, data):
    get(conn, weight_trials, data.trial)
    row = conn.execute(select(trial_entries)
                       .where(trial_entries.c.trial == data.trial,
                              trial_entries.c.entrance == data.entrance)
                       .with_for_update()).mappings().first()
    need(row is not None, f'入口 {data.entrance} 不在试算批次')
    judgment = '走得过' if data.passable else '走不过'
    if row['judgment'] is not None:
        need(row['judgment'] != judgment, '现场判定未变化')
        need(user['role'] == 'reviewer', '改判须由复核员执行')
        cause, force = '复核改判', True
    else:
        cause, force = '判定齐', False
    conn.execute(trial_entries.update()
                 .where(trial_entries.c.trial == data.trial,
                        trial_entries.c.entrance == data.entrance).values(judgment=judgment))
    settled = settle(conn, data.trial, cause=cause, force=force)
    return {'trial': data.trial, 'entrance': data.entrance, 'judgment': judgment, 'settled': settled}


def score_trial(conn, user, data):
    get(conn, weight_trials, data.trial)
    return submit(user, {'kind': 'weight_trial_scoring', 'trial': data.trial})


def false_passes(conn, user, data):
    trial = get(conn, weight_trials, data.trial)
    entries = entries_of(conn, data.trial)
    need(entries and all(row['judgment'] is not None and row['score_a'] is not None
                         and row['score_b'] is not None for row in entries),
         '现场判定或两套分未齐，尚无结论')
    return {'trial': data.trial,
            '现行权重误放': false_passed(entries, 'score_a', trial['threshold']) or ['无'],
            '候选权重误放': false_passed(entries, 'score_b', trial['threshold']) or ['无']}


def conclusion_log(conn, user, data):
    get(conn, weight_trials, data.trial)
    rows = conn.execute(select(trial_conclusions).where(trial_conclusions.c.trial == data.trial)
                        .order_by(trial_conclusions.c.id)).mappings()
    log = [{'时间': row['at'], '事由': row['cause'], '现行误放': row['false_pass_a'],
            '候选误放': row['false_pass_b'], '结论': row['verdict']} for row in rows]
    need(log, '尚未形成结论')
    return {'trial': data.trial, '结论留档': log}
