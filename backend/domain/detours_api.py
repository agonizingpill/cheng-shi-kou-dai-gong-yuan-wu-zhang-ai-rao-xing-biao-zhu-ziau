from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import detours_service as service
from domain.detours_model import detours
from domain.detours_schemas import SubmitDetour, WithdrawDetour

router = APIRouter()

@router.get('/detours')
def list_detours(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, detours)


@router.post('/detours/submit-detour')
def submit_detour(data: SubmitDetour, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.submit_detour(conn, user, data)
        record(conn, user, 'detours.submit_detour')
        return output


@router.post('/detours/withdraw-detour')
def withdraw_detour(data: WithdrawDetour, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.withdraw_detour(conn, user, data)
        record(conn, user, 'detours.withdraw_detour')
        return output
