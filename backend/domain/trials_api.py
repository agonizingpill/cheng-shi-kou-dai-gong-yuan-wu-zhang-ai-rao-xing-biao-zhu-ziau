from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from domain import trials_service as service
from domain.trials_schemas import DraftTrial, JudgeEntry, ScoreTrial, TrialQuery

router = APIRouter()

@router.get('/trials')
def list_trials(user=Depends(actor)):
    with transaction() as conn:
        return service.list_trials(conn)


@router.post('/trials/draft-trial')
def draft_trial(data: DraftTrial, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.draft_trial(conn, user, data)
        record(conn, user, 'trials.draft_trial')
        return output


@router.post('/trials/judge-entry')
def judge_entry(data: JudgeEntry, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.judge_entry(conn, user, data)
        record(conn, user, 'trials.judge_entry')
        return output


@router.post('/trials/score')
def score_trial(data: ScoreTrial, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.score_trial(conn, user, data)
        record(conn, user, 'trials.score')
        return output


@router.post('/trials/false-passes')
def false_passes(data: TrialQuery, user=Depends(actor)):
    with transaction() as conn:
        return service.false_passes(conn, user, data)


@router.post('/trials/conclusion-log')
def conclusion_log(data: TrialQuery, user=Depends(actor)):
    with transaction() as conn:
        return service.conclusion_log(conn, user, data)
