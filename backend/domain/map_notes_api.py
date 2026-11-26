from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import map_notes_service as service
from domain.map_notes_model import map_notes
from domain.map_notes_schemas import PublishMap

router = APIRouter()

@router.get('/map_notes')
def list_map_notes(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, map_notes)


@router.post('/map_notes/publish-map')
def publish_map(data: PublishMap, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.publish_map(conn, user, data)
        record(conn, user, 'map_notes.publish_map')
        return output
