from sqladmin import ModelView

from src.instructions.models import Instruction


class InstructionAdmin(ModelView, model=Instruction):
    column_list = [
        Instruction.title,
        Instruction.description,
    ]
    can_export = False
