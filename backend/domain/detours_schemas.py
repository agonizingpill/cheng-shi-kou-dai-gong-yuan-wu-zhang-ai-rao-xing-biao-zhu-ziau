from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class SubmitDetour(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    entrance: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    walk_m: int


class WithdrawDetour(BaseModel):
    model_config = ConfigDict(extra="forbid")
    detour: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
