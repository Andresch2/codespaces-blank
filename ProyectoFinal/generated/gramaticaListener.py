# Generated from gramatica.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# This class defines a complete listener for a parse tree produced by gramaticaParser.
class gramaticaListener(ParseTreeListener):

    # Enter a parse tree produced by gramaticaParser#program.
    def enterProgram(self, ctx:gramaticaParser.ProgramContext):
        pass

    # Exit a parse tree produced by gramaticaParser#program.
    def exitProgram(self, ctx:gramaticaParser.ProgramContext):
        pass


    # Enter a parse tree produced by gramaticaParser#statement.
    def enterStatement(self, ctx:gramaticaParser.StatementContext):
        pass

    # Exit a parse tree produced by gramaticaParser#statement.
    def exitStatement(self, ctx:gramaticaParser.StatementContext):
        pass


    # Enter a parse tree produced by gramaticaParser#assignment.
    def enterAssignment(self, ctx:gramaticaParser.AssignmentContext):
        pass

    # Exit a parse tree produced by gramaticaParser#assignment.
    def exitAssignment(self, ctx:gramaticaParser.AssignmentContext):
        pass


    # Enter a parse tree produced by gramaticaParser#ruleStmt.
    def enterRuleStmt(self, ctx:gramaticaParser.RuleStmtContext):
        pass

    # Exit a parse tree produced by gramaticaParser#ruleStmt.
    def exitRuleStmt(self, ctx:gramaticaParser.RuleStmtContext):
        pass


    # Enter a parse tree produced by gramaticaParser#action.
    def enterAction(self, ctx:gramaticaParser.ActionContext):
        pass

    # Exit a parse tree produced by gramaticaParser#action.
    def exitAction(self, ctx:gramaticaParser.ActionContext):
        pass


    # Enter a parse tree produced by gramaticaParser#cond.
    def enterCond(self, ctx:gramaticaParser.CondContext):
        pass

    # Exit a parse tree produced by gramaticaParser#cond.
    def exitCond(self, ctx:gramaticaParser.CondContext):
        pass


    # Enter a parse tree produced by gramaticaParser#printStmt.
    def enterPrintStmt(self, ctx:gramaticaParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by gramaticaParser#printStmt.
    def exitPrintStmt(self, ctx:gramaticaParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by gramaticaParser#expr.
    def enterExpr(self, ctx:gramaticaParser.ExprContext):
        pass

    # Exit a parse tree produced by gramaticaParser#expr.
    def exitExpr(self, ctx:gramaticaParser.ExprContext):
        pass


    # Enter a parse tree produced by gramaticaParser#term.
    def enterTerm(self, ctx:gramaticaParser.TermContext):
        pass

    # Exit a parse tree produced by gramaticaParser#term.
    def exitTerm(self, ctx:gramaticaParser.TermContext):
        pass


    # Enter a parse tree produced by gramaticaParser#factor.
    def enterFactor(self, ctx:gramaticaParser.FactorContext):
        pass

    # Exit a parse tree produced by gramaticaParser#factor.
    def exitFactor(self, ctx:gramaticaParser.FactorContext):
        pass


    # Enter a parse tree produced by gramaticaParser#comparator.
    def enterComparator(self, ctx:gramaticaParser.ComparatorContext):
        pass

    # Exit a parse tree produced by gramaticaParser#comparator.
    def exitComparator(self, ctx:gramaticaParser.ComparatorContext):
        pass



del gramaticaParser