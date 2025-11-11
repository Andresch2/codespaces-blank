# Generated from gramatica.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# This class defines a complete generic visitor for a parse tree produced by gramaticaParser.

class gramaticaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by gramaticaParser#program.
    def visitProgram(self, ctx:gramaticaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#statement.
    def visitStatement(self, ctx:gramaticaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#assignment.
    def visitAssignment(self, ctx:gramaticaParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#ruleStmt.
    def visitRuleStmt(self, ctx:gramaticaParser.RuleStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#action.
    def visitAction(self, ctx:gramaticaParser.ActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#cond.
    def visitCond(self, ctx:gramaticaParser.CondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#printStmt.
    def visitPrintStmt(self, ctx:gramaticaParser.PrintStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#expr.
    def visitExpr(self, ctx:gramaticaParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#term.
    def visitTerm(self, ctx:gramaticaParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#factor.
    def visitFactor(self, ctx:gramaticaParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#comparator.
    def visitComparator(self, ctx:gramaticaParser.ComparatorContext):
        return self.visitChildren(ctx)



del gramaticaParser