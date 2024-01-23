from typing import Optional
from pydantic import BaseModel, constr

from .models import Instruction

TITLE_LEN = Instruction.title.type.length
DESCRIPTION_LEN = Instruction.description.type.length


class GetInstructionSchema(BaseModel):
    id: int
    title: constr(max_length=TITLE_LEN)
    description: constr(max_length=DESCRIPTION_LEN)


class UpdateInstructionSchema(BaseModel):
    title: Optional[constr(max_length=TITLE_LEN)] = None
    description: Optional[constr(max_length=DESCRIPTION_LEN)] = None
