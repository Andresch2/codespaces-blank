# -*- coding: utf-8 -*-
# IR muy simple y textual para mostrar la fase intermedia

from dataclasses import dataclass
from typing import List

@dataclass
class IRInstr:
    def to_text(self) -> str:
        raise NotImplementedError

@dataclass
class IRAssign(IRInstr):
    name: str
    expr_py: str  # expresión serializada a Python
    def to_text(self) -> str:
        return f"ASSIGN {self.name} := {self.expr_py}"

@dataclass
class IRIfAssign(IRInstr):
    var: str
    op: str
    rhs_py: str
    target: str
    value_py: str
    def to_text(self) -> str:
        return f"IF {self.var} {self.op} {self.rhs_py} THEN {self.target} := {self.value_py}"

@dataclass
class IRPrint(IRInstr):
    name: str
    def to_text(self) -> str:
        return f"PRINT {self.name}"

@dataclass
class IRProgram:
    instructions: List[IRInstr]
    def to_text(self) -> str:
        return "\n".join(instr.to_text() for instr in self.instructions)
