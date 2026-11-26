from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class Inspect(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entrance: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    ramp: bool
