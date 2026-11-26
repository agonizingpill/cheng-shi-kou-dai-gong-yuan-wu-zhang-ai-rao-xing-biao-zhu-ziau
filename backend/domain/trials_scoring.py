from datetime import datetime, timezone

from sqlalchemy import select

from core.db import transaction
from core.records import get
from domain.trials_model import trial_conclusions, trial_entries, weight_trials
from domain.walk_profiles_model import walk_profiles


def score(tags, weights):
    total = sum(weights.values())
    overlap = sum(weights[tag] for tag in tags if tag in weights)
    return round(1 - overlap / total, 4)


def entries_of(conn, trial_code):
    rows = conn.execute(select(trial_entries).where(trial_entries.c.trial == trial_code)
                        .order_by(trial_entries.c.entrance)).mappings()
    return [dict(row) for row in rows]


def false_passed(entries, key, threshold):
    return sorted(row['entrance'] for row in entries
                  if row[key] >= threshold and row['judgment'] == '走不过')


def latest_conclusion(conn, trial_code):
    return conn.execute(select(trial_conclusions).where(trial_conclusions.c.trial == trial_code)
                        .order_by(trial_conclusions.c.id.desc()).limit(1)).mappings().first()


def settle(conn, trial_code, cause, force=False):
    trial = get(conn, weight_trials, trial_code, lock=True)
    entries = entries_of(conn, trial_code)
    complete = entries and all(row['judgment'] is not None and row['score_a'] is not None
                               and row['score_b'] is not None for row in entries)
    if not complete:
        return False
    missed_a = false_passed(entries, 'score_a', trial['threshold'])
    missed_b = false_passed(entries, 'score_b', trial['threshold'])
    latest = latest_conclusion(conn, trial_code)
    if not force and latest and latest['false_pass_a'] == len(missed_a) and latest['false_pass_b'] == len(missed_b):
        return False
    verdict = ('候选权重误放更多' if len(missed_b) > len(missed_a)
               else '现行权重误放更多' if len(missed_a) > len(missed_b) else '两套误放持平')
    conn.execute(trial_conclusions.insert().values(
        trial=trial_code, false_pass_a=len(missed_a), false_pass_b=len(missed_b),
        verdict=verdict, cause=cause, at=datetime.now(timezone.utc)))
    conn.execute(weight_trials.update().where(weight_trials.c.code == trial_code).values(state='已结论'))
    return True


def score_pending(trial_code):
    with transaction() as conn:
        trial = get(conn, weight_trials, trial_code)
        profile = get(conn, walk_profiles, trial['profile'])
        pending = [row for row in entries_of(conn, trial_code)
                   if row['score_a'] is None or row['score_b'] is None]
        reused = len(entries_of(conn, trial_code)) - len(pending)
    for row in pending:
        with transaction() as conn:
            current = conn.execute(select(trial_entries)
                                   .where(trial_entries.c.trial == trial_code,
                                          trial_entries.c.entrance == row['entrance'])
                                   .with_for_update()).mappings().one()
            updates = {}
            if current['score_a'] is None:
                updates['score_a'] = score(current['tags'], profile['weights'])
            if current['score_b'] is None:
                updates['score_b'] = score(current['tags'], trial['weights_b'])
            if updates:
                conn.execute(trial_entries.update()
                             .where(trial_entries.c.trial == trial_code,
                                    trial_entries.c.entrance == row['entrance']).values(**updates))
    with transaction() as conn:
        settled = settle(conn, trial_code, cause='评分齐')
    return {'trial': trial_code, 'scored': len(pending), 'reused': reused, 'settled': settled}
