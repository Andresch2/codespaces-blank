# -*- coding: utf-8 -*-
# Recorro el parse tree y construyo mi AST

from antlr4 import ParserRuleContext
from generated.gramaticaVisitor import gramaticaVisitor
from generated.gramaticaParser import gramaticaParser
from semantic_analyzer.ast_nodes import *

def _pos(ctx: ParserRuleContext):
    return (ctx.start.line if ctx.start else 0,
            ctx.start.column if ctx.start else 0)

class ASTBuilder(gramaticaVisitor):
    """Convierte el árbol sintáctico (parse tree) en nuestro AST con nodos simples."""

    # program: statement+ EOF ;
    def visitProgram(self, ctx: gramaticaParser.ProgramContext):
        stmts = [self.visit(s) for s in ctx.statement()]
        return Program(statements=stmts)

    # statement: assignment | ruleStmt | printStmt ;
    def visitStatement(self, ctx: gramaticaParser.StatementContext):
        if ctx.assignment():  return self.visit(ctx.assignment())
        if ctx.ruleStmt():    return self.visit(ctx.ruleStmt())
        if ctx.printStmt():   return self.visit(ctx.printStmt())
        raise RuntimeError("Alternativa de statement no reconocida")

    # assignment: ID '=' expr ';' ;
    def visitAssignment(self, ctx: gramaticaParser.AssignmentContext):
        name = ctx.ID().getText()
        expr = self.visit(ctx.expr())
        line, col = _pos(ctx)
        return Assignment(name=name, expr=expr, line=line, col=col)

    # ruleStmt: SI cond ':' action ;
    def visitRuleStmt(self, ctx: gramaticaParser.RuleStmtContext):
        cond = self.visit(ctx.cond())
        action = self.visit(ctx.action())
        line, col = _pos(ctx)
        return Rule(cond=cond, action=action, line=line, col=col)

    # action: ID '=' expr ';' ;
    def visitAction(self, ctx: gramaticaParser.ActionContext):
        name = ctx.ID().getText()
        expr = self.visit(ctx.expr())
        line, col = _pos(ctx)
        return Action(name=name, expr=expr, line=line, col=col)

    # cond: ID comparator expr ;
    def visitCond(self, ctx: gramaticaParser.CondContext):
        var = ctx.ID().getText()
        op = ctx.comparator().getText()
        rhs = self.visit(ctx.expr())
        line, col = _pos(ctx)
        return Cond(var=var, op=op, rhs=rhs, line=line, col=col)

    # printStmt: PRINT '(' ID ')' ';' ;
    def visitPrintStmt(self, ctx: gramaticaParser.PrintStmtContext):
        name = ctx.ID().getText()
        line, col = _pos(ctx)
        return PrintStmt(name=name, line=line, col=col)

    # ===== Expresiones =====
    # expr: expr ('+'|'-') term | term ;
    def visitExpr(self, ctx: gramaticaParser.ExprContext):
        if ctx.getChildCount() == 1:      # solo term
            return self.visit(ctx.getChild(0))
        # expr op term
        left = self.visit(ctx.getChild(0))
        op   = ctx.getChild(1).getText()
        right= self.visit(ctx.getChild(2))
        line, col = _pos(ctx)
        return BinOp(left=left, op=op, right=right, line=line, col=col)

    # term: term ('*'|'/') factor | factor ;
    def visitTerm(self, ctx: gramaticaParser.TermContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        left = self.visit(ctx.getChild(0))
        op   = ctx.getChild(1).getText()
        right= self.visit(ctx.getChild(2))
        line, col = _pos(ctx)
        return BinOp(left=left, op=op, right=right, line=line, col=col)

    # factor: NUMBER | ID | '(' expr ')' ;
    def visitFactor(self, ctx: gramaticaParser.FactorContext):
        child = ctx.getChild(0)
        text  = child.getText()
        line, col = _pos(ctx)

        # ID
        if text.isidentifier():
            return Var(name=text, line=line, col=col)

        # NUMBER (entero o float)
        if self._is_number(text):
            return Number(value=float(text), line=line, col=col)

        # '(' expr ')'
        return self.visit(ctx.getChild(1))

    def _is_number(self, s: str) -> bool:
        try:
            float(s); return True
        except:
            return False
