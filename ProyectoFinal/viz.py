# viz.py
from graphviz import Digraph
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4 import ParserRuleContext
from antlr4.tree.Trees import Trees

# ---- Parse tree (árbol de sintaxis concreta) ----
def render_parse_tree(tree, parser, out_basepath):
    dot = Digraph('parse', node_attr={'shape': 'box', 'fontname': 'Helvetica', 'fontsize': '10'})
    counter = 0

    def add(n):
        nonlocal counter
        nid = f"n{counter}"; counter += 1
        if isinstance(n, TerminalNodeImpl):
            label = Trees.getNodeText(n, ruleNames=parser.ruleNames)
        else:
            rule_index = n.getRuleIndex()
            label = parser.ruleNames[rule_index]
        dot.node(nid, label)
        if isinstance(n, ParserRuleContext):
            for i in range(n.getChildCount()):
                c = n.getChild(i)
                cid = add(c)
                dot.edge(nid, cid)
        return nid

    add(tree)
    dot.render(out_basepath, format='svg', cleanup=True)  # genera out_basepath.svg

# ---- AST (árbol de sintaxis abstracta) ----
from semantic_analyzer.ast_nodes import (
    Program, Assignment, Rule, Action, PrintStmt, Cond, BinOp, Number, Var
)

def render_ast(ast, out_basepath):
    dot = Digraph('ast', node_attr={'shape': 'ellipse', 'fontname': 'Helvetica', 'fontsize': '10'})
    counter = 0

    def visit(node):
        nonlocal counter
        nid = f"n{counter}"; counter += 1

        if isinstance(node, Program):
            dot.node(nid, "Program", shape='box')
            for st in node.statements:
                dot.edge(nid, visit(st))

        elif isinstance(node, Assignment):
            dot.node(nid, f"Assignment\\n{node.name}", shape='box')
            dot.edge(nid, visit(node.expr))

        elif isinstance(node, Rule):
            dot.node(nid, "Rule", shape='box')
            dot.edge(nid, visit(node.cond))
            dot.edge(nid, visit(node.action))

        elif isinstance(node, Action):
            dot.node(nid, f"Action\\n{node.name}", shape='box')
            dot.edge(nid, visit(node.expr))

        elif isinstance(node, Cond):
            dot.node(nid, f"Cond\\n{node.var} {node.op}")
            dot.edge(nid, visit(node.rhs))

        elif isinstance(node, PrintStmt):
            dot.node(nid, f"Print\\n{node.name}")

        elif isinstance(node, BinOp):
            dot.node(nid, f"BinOp\\n{node.op}")
            dot.edge(nid, visit(node.left))
            dot.edge(nid, visit(node.right))

        elif isinstance(node, Number):
            dot.node(nid, f"Number\\n{node.value}")

        elif isinstance(node, Var):
            dot.node(nid, f"Var\\n{node.name}")

        else:
            dot.node(nid, type(node).__name__)

        return nid

    visit(ast)
    dot.render(out_basepath, format='svg', cleanup=True)  # genera out_basepath.svg
