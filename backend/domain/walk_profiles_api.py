from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import walk_profiles_service as service
from domain.walk_profiles_model import walk_profiles
from domain.walk_profiles_schemas import DraftProfile, MatchEntrances

router = APIRouter()

@router.get('/walk_profiles')
def list_walk_profiles(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, walk_profiles)


@router.post('/walk_profiles/draft-profile')
def draft_profile(data: DraftProfile, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.draft_profile(conn, user, data)
        record(conn, user, 'walk_profiles.draft_profile')
        return output


@router.post('/walk_profiles/match-entrances')
def match_entrances(data: MatchEntrances, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.match_entrances(conn, user, data)
        record(conn, user, 'walk_profiles.match_entrances')
        return output
