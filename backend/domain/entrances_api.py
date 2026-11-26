from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import entrances_service as service
from domain.entrances_model import entrances
from domain.entrances_schemas import Inspect

router = APIRouter()

@router.get('/entrances')
def list_entrances(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, entrances)


@router.post('/entrances/inspect')
def inspect(data: Inspect, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.inspect(conn, user, data)
        record(conn, user, 'entrances.inspect')
        return output
