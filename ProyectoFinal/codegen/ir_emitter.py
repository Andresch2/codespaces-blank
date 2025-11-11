# -*- coding: utf-8 -*-
# Convierte el AST a nuestra IR
from typing import List
from semantic_analyzer.ast_nodes import *
from codegen.ir import *

class IREmitter:
    def _expr_to_py(self, e: Expr) -> str:
        # Serializa la expresión AST a una cadena Python
        if isinstance(e, Number):
            if float(e.value).is_integer():
                return str(int(e.value))
            return str(e.value)
        if isinstance(e, Var):
            return e.name
        if isinstance(e, BinOp):
            left = self._expr_to_py(e.left)
            right = self._expr_to_py(e.right)
            return f"({left} {e.op} {right})"
        raise RuntimeError("Expresión no soportada en codegen")

    def to_ir(self, program: Program) -> IRProgram:
        instrs: List[IRInstr] = []
        for st in program.statements:
            if isinstance(st, Assignment):
                instrs.append(IRAssign(name=st.name, expr_py=self._expr_to_py(st.expr)))
            elif isinstance(st, Rule):
                rhs_py = self._expr_to_py(st.cond.rhs)
                act_py = self._expr_to_py(st.action.expr)
                instrs.append(IRIfAssign(
                    var=st.cond.var, op=st.cond.op, rhs_py=rhs_py,
                    target=st.action.name, value_py=act_py
                ))
            elif isinstance(st, PrintStmt):
                instrs.append(IRPrint(name=st.name))
            else:
                raise RuntimeError("Sentencia no soportada en IR")
        return IRProgram(instructions=instrs)
