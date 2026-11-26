from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class DraftProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    park: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    avoid: list | dict
    weights: list | dict
    minimum: FiniteFloat


class MatchEntrances(BaseModel):
    model_config = ConfigDict(extra="forbid")
    profile: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
