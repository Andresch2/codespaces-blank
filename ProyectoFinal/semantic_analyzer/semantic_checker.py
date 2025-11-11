# -*- coding: utf-8 -*-
# Reglas:
# - Variables usadas en RHS (expr) y en print() deben estar definidas previamente.
# - La variable de la condición (cond.var) debe estar definida previamente.
# - Chequeo estático: división por cero literal (x / 0).

from semantic_analyzer.ast_nodes import *
from semantic_analyzer.symbol_table import SymbolTable

class SemanticError(Exception):
    pass

class SemanticChecker:
    def __init__(self):
        self.sym = SymbolTable()

    def check(self, program: Program):
        for st in program.statements:
            if isinstance(st, Assignment):
                self._check_expr_vars_defined(st.expr)
                self.sym.define(st.name)

            elif isinstance(st, Rule):
                if not self.sym.is_defined(st.cond.var):
                    raise SemanticError(f"Linea {st.cond.line}:{st.cond.col} - Variable no declarada en condición: '{st.cond.var}'")
                self._check_expr_vars_defined(st.cond.rhs)
                self._check_expr_vars_defined(st.action.expr)
                self.sym.define(st.action.name)

            elif isinstance(st, PrintStmt):
                if not self.sym.is_defined(st.name):
                    raise SemanticError(f"Linea {st.line}:{st.col} - print de variable no declarada: '{st.name}'")
            else:
                raise SemanticError("Sentencia no soportada")

    def _check_expr_vars_defined(self, expr: Expr):
        if isinstance(expr, Var):
            if not self.sym.is_defined(expr.name):
                raise SemanticError(f"Linea {expr.line}:{expr.col} - Variable no declarada: '{expr.name}'")
        elif isinstance(expr, Number):
            return
        elif isinstance(expr, BinOp):
            self._check_expr_vars_defined(expr.left)
            self._check_expr_vars_defined(expr.right)
            if expr.op == '/' and self._is_zero(expr.right):
                raise SemanticError(f"Linea {expr.line}:{expr.col} - División por cero literal")
        else:
            raise SemanticError("Expresión no soportada")

    def _is_zero(self, expr: Expr) -> bool:
        return isinstance(expr, Number) and abs(expr.value) == 0.0

    def dump_symbols(self) -> str:
        return self.sym.dump()
