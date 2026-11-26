from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

Code = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]

class DraftTrial(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Code
    profile: Code
    weights_b: list | dict
    threshold: FiniteFloat


class JudgeEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trial: Code
    entrance: Code
    passable: bool


class ScoreTrial(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trial: Code


class TrialQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trial: Code
