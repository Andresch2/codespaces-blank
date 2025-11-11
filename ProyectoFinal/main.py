# -*- coding: utf-8 -*-
# Ejecuta TODAS las fases y genera artefactos por test:
# 1_tokens.txt, 2_parse_tree.txt, 3_ast.txt, 4_symbols.txt, 5_ir.txt, 6_output_program.py, 7_stdout.txt

import argparse, os, sys, subprocess, pathlib
from antlr4 import CommonTokenStream, FileStream
from antlr4.tree.Trees import Trees
from antlr4.error.ErrorListener import ErrorListener

# IMPORTS AJUSTADOS A grammar gramatica;
from generated.gramaticaLexer import gramaticaLexer
from generated.gramaticaParser import gramaticaParser

from semantic_analyzer.ast_builder import ASTBuilder
from semantic_analyzer.semantic_checker import SemanticChecker, SemanticError
from codegen.ir_emitter import IREmitter
from codegen.python_codegen import PythonCodegen

# ===== ErrorListener que "lanza" en el primer error léxico/sintáctico =====
class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"line {line}:{column} {msg}")

def read_meta(src_path: str):
    """Lee cabecera // @title y // @expect del test .txt (opcional)."""
    title = os.path.basename(src_path)
    expect = "ok"
    with open(src_path, "r", encoding="utf-8") as f:
        for line in f:
            ls = line.strip()
            if ls.startswith("// @title:"):
                title = ls.split(":", 1)[1].strip()
            elif ls.startswith("// @expect:"):
                expect = ls.split(":", 1)[1].strip()
            if ls == "" or not ls.startswith("//"):
                break
    return title, expect

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def write_artifact(dirpath: str, name: str, content: str):
    ensure_dir(dirpath)
    with open(os.path.join(dirpath, name), "w", encoding="utf-8") as f:
        f.write(content if content is not None else "")

def compile_one(src_path: str, artifacts_root="artifacts") -> int:
    title, _ = read_meta(src_path)
    base = pathlib.Path(src_path).stem
    outdir = os.path.join(artifacts_root, base)
    ensure_dir(outdir)

    # ====== LÉXICO + SINTAXIS ======
    try:
        stream = FileStream(src_path, encoding="utf-8")
        lexer  = gramaticaLexer(stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(ThrowingErrorListener())    # errores léxicos => excepción

        tokens = CommonTokenStream(lexer)
        tokens.fill()
        # dump de tokens
        tok_dump = "\n".join([f"{t.text}\t(type={t.type}, line={t.line}, col={t.column})" for t in tokens.tokens])
        write_artifact(outdir, "1_tokens.txt", tok_dump)

        parser = gramaticaParser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(ThrowingErrorListener())   # errores sintácticos => excepción

        tree   = parser.program()
        parse_tree_str = Trees.toStringTree(tree, None, parser)
        write_artifact(outdir, "2_parse_tree.txt", parse_tree_str)
    except Exception as e:
        write_artifact(outdir, "ERROR_lex_syn.txt", f"[LEX/SYN] {e}")
        return 1  # falló temprano

    # ====== AST + SEMÁNTICA ======
    try:
        ast = ASTBuilder().visit(tree)
        write_artifact(outdir, "3_ast.txt", ast.pretty())

        checker = SemanticChecker()
        checker.check(ast)
        write_artifact(outdir, "4_symbols.txt", checker.dump_symbols())
    except SemanticError as e:
        write_artifact(outdir, "ERROR_semantic.txt", f"[SEM] {e}")
        return 1
    except Exception as e:
        write_artifact(outdir, "ERROR_semantic.txt", f"[SEM-EXCEP] {e}")
        return 1

    # ====== IR + PYTHON + EJECUCIÓN ======
    ir = IREmitter().to_ir(ast)
    write_artifact(outdir, "5_ir.txt", ir.to_text())

    py_code = PythonCodegen().emit(ir)
    py_path = os.path.join(outdir, "6_output_program.py")
    write_artifact(outdir, "6_output_program.py", py_code)

    try:
        result = subprocess.run([sys.executable, py_path], capture_output=True, text=True, timeout=5)
        write_artifact(outdir, "7_stdout.txt", result.stdout)
        write_artifact(outdir, "7_stderr.txt", result.stderr)
        return 0 if result.returncode == 0 else 1
    except Exception as e:
        write_artifact(outdir, "ERROR_runtime.txt", f"[RUNTIME] {e}")
        return 1

def main():
    ap = argparse.ArgumentParser(description="Mini-compiler (gramatica → Python)")
    # --- CAMBIO: --src ahora es opcional y por defecto usa input.txt ---
    ap.add_argument("--src", required=False, default="input.txt",
                    help="ruta del archivo .txt del lenguaje; por defecto usa ./input.txt")
    # --- CAMBIO: flag para silenciar la impresión en consola ---
    ap.add_argument("--quiet", action="store_true",
                    help="no imprimir la salida del programa generado en consola")
    args = ap.parse_args()

    # Si no existe el archivo, avisamos claramente (no rompe nada de tests)
    if not os.path.exists(args.src):
        print(f"[ERROR] No existe el archivo: {args.src}")
        print("Crea un 'input.txt' en la raíz o especifica --src tests/valid/V1.txt, etc.")
        sys.exit(1)

    # Compilar y generar artefactos
    rc = compile_one(args.src)

    # Si estamos en modo simple (input.txt por defecto) y no está silenciado, mostramos stdout del programa generado
    if not args.quiet:
        base = pathlib.Path(args.src).stem
        outdir = os.path.join("artifacts", base)
        stdout_path = os.path.join(outdir, "7_stdout.txt")
        err_lexsyn = os.path.join(outdir, "ERROR_lex_syn.txt")
        err_sem    = os.path.join(outdir, "ERROR_semantic.txt")
        err_run    = os.path.join(outdir, "ERROR_runtime.txt")

        # Imprime stdout si existe; si no, imprime el error correspondiente
        if os.path.exists(stdout_path) and rc == 0:
            with open(stdout_path, "r", encoding="utf-8") as f:
                print(f.read(), end="")  # sin línea extra
        else:
            err_to_show = None
            for p in (err_lexsyn, err_sem, err_run):
                if os.path.exists(p):
                    err_to_show = p; break
            if err_to_show:
                with open(err_to_show, "r", encoding="utf-8") as f:
                    print(f.read(), end="")

        print(f"\n[artefactos] {outdir}")

    sys.exit(rc)

if __name__ == "__main__":
    main()
