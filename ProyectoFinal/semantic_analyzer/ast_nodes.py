# -*- coding: utf-8 -*-
# Nodos del AST + pretty-print

from dataclasses import dataclass
from typing import List

# ==== Expresiones ====
@dataclass
class Expr:
    line: int = 0
    col: int = 0
    def pretty(self, indent=0) -> str:
        raise NotImplementedError

@dataclass
class Number(Expr):
    value: float = 0.0
    def pretty(self, indent=0) -> str:
        return " " * indent + f"Number({self.value})"

@dataclass
class Var(Expr):
    name: str = ""
    def pretty(self, indent=0) -> str:
        return " " * indent + f"Var({self.name})"

@dataclass
class BinOp(Expr):
    left: Expr = None
    op: str = ""
    right: Expr = None
    def pretty(self, indent=0) -> str:
        s = " " * indent + f"BinOp('{self.op}')\n"
        s += self.left.pretty(indent + 2) + "\n"
        s += self.right.pretty(indent + 2)
        return s

# ==== Condición ====
@dataclass
class Cond:
    var: str
    op: str
    rhs: Expr
    line: int = 0
    col: int = 0
    def pretty(self, indent=0) -> str:
        s = " " * indent + f"Cond({self.var} {self.op} ...)\n"
        s += self.rhs.pretty(indent + 2)
        return s

# ==== Sentencias ====
@dataclass
class Stmt:
    line: int = 0
    col: int = 0
    def pretty(self, indent=0) -> str:
        raise NotImplementedError

@dataclass
class Assignment(Stmt):
    name: str = ""
    expr: Expr = None
    def pretty(self, indent=0) -> str:
        s = " " * indent + f"Assignment({self.name})\n"
        s += self.expr.pretty(indent + 2)
        return s

@dataclass
class Action(Stmt):
    name: str = ""
    expr: Expr = None
    def pretty(self, indent=0) -> str:
        s = " " * indent + f"Action({self.name})\n"
        s += self.expr.pretty(indent + 2)
        return s

@dataclass
class Rule(Stmt):
    cond: Cond = None
    action: Action = None
    def pretty(self, indent=0) -> str:
        s = " " * indent + "Rule\n"
        s += self.cond.pretty(indent + 2) + "\n"
        s += self.action.pretty(indent + 2)
        return s

@dataclass
class PrintStmt(Stmt):
    name: str = ""
    def pretty(self, indent=0) -> str:
        return " " * indent + f"Print({self.name})"

# ==== Programa ====
@dataclass
class Program:
    statements: List[Stmt]
    def pretty(self, indent=0) -> str:
        s = " " * indent + "Program\n"
        for i, st in enumerate(self.statements):
            s += st.pretty(indent + 2)
            if i < len(self.statements) - 1:
                s += "\n"
        return s
