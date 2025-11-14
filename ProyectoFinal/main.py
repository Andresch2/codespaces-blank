# -*- coding: utf-8 -*-
# Ejecuta TODAS las fases y genera artefactos por test:
# 1_tokens.txt, 2_parse_tree.txt, 3_ast.txt, 4_symbols.txt, 5_ir.txt, 6_output_program.py, 7_stdout.txt
# Además, SOLO cuando el src sea input.txt, en la RAÍZ deja: output_program.py y output.txt
# Y SIEMPRE genera artifacts/<CASO>/output.txt con resumen del caso.
#
# Comportamiento de consola:
# - Por defecto: imprime fases + explicación de errores.
# - Con --quiet: no imprime nada (compat con run_tests.py).

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

# Visualización (no obligatoria): si falta graphviz o el módulo, no rompe
try:
    from viz import render_parse_tree, render_ast
except Exception:
    render_parse_tree = None
    render_ast = None

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
    base = pathlib.Path(src_path).stem
    outdir = os.path.join(artifacts_root, base)
    ensure_dir(outdir)

    # ====== LÉXICO + SINTAXIS ======
    try:
        stream = FileStream(src_path, encoding="utf-8")
        lexer  = gramaticaLexer(stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(ThrowingErrorListener())

        tokens = CommonTokenStream(lexer)
        tokens.fill()
        tok_dump = "\n".join([f"{t.text}\t(type={t.type}, line={t.line}, col={t.column})" for t in tokens.tokens])
        write_artifact(outdir, "1_tokens.txt", tok_dump)

        parser = gramaticaParser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(ThrowingErrorListener())

        tree   = parser.program()
        parse_tree_str = Trees.toStringTree(tree, None, parser)
        write_artifact(outdir, "2_parse_tree.txt", parse_tree_str)

        if render_parse_tree is not None:
            try:
                render_parse_tree(tree, parser, os.path.join(outdir, "2_parse_tree"))
            except Exception as ve:
                write_artifact(outdir, "WARN_viz_parse.txt", f"parse tree viz failed: {ve}")

    except Exception as e:
        msg = f"[LEX/SYN] {e}"
        write_artifact(outdir, "ERROR_lex_syn.txt", msg)
        write_artifact(outdir, "output.txt",
                       f"[source] {src_path}\n[status] error\n[type] lex/syn\n[msg] {e}\n")
        return 1

    # ====== AST + SEMÁNTICA ======
    try:
        ast = ASTBuilder().visit(tree)
        write_artifact(outdir, "3_ast.txt", ast.pretty())

        if render_ast is not None:
            try:
                render_ast(ast, os.path.join(outdir, "3_ast"))
            except Exception as ve:
                write_artifact(outdir, "WARN_viz_ast.txt", f"ast viz failed: {ve}")

        checker = SemanticChecker()
        checker.check(ast)
        write_artifact(outdir, "4_symbols.txt", checker.dump_symbols())
    except SemanticError as e:
        msg = f"[SEM] {e}"
        write_artifact(outdir, "ERROR_semantic.txt", msg)
        write_artifact(outdir, "output.txt",
                       f"[source] {src_path}\n[status] error\n[type] sem\n[msg] {e}\n")
        return 1
    except Exception as e:
        msg = f"[SEM-EXCEP] {e}"
        write_artifact(outdir, "ERROR_semantic.txt", msg)
        write_artifact(outdir, "output.txt",
                       f"[source] {src_path}\n[status] error\n[type] sem\n[msg] {e}\n")
        return 1

    # ====== IR + PYTHON + EJECUCIÓN ======
    ir = IREmitter().to_ir(ast)
    write_artifact(outdir, "5_ir.txt", ir.to_text())

    py_code = PythonCodegen().emit(ir)
    py_path = os.path.join(outdir, "6_output_program.py")
    write_artifact(outdir, "6_output_program.py", py_code)

    is_root_case = (os.path.basename(src_path) == "input.txt") or (
        os.path.abspath(src_path) == os.path.abspath("input.txt")
    )

    try:
        result = subprocess.run([sys.executable, py_path], capture_output=True, text=True, timeout=5)
        write_artifact(outdir, "7_stdout.txt", result.stdout)
        write_artifact(outdir, "7_stderr.txt", result.stderr)

        case_summary = []
        case_summary.append(f"[source] {src_path}")
        case_summary.append("[status] ok")
        case_summary.append("[python] 6_output_program.py")
        case_summary.append(f"[returncode] {result.returncode}")
        if result.stdout:
            case_summary.append("\n[stdout]\n" + result.stdout.strip())
        if result.stderr:
            case_summary.append("\n[stderr]\n" + result.stderr.strip())
        write_artifact(outdir, "output.txt", "\n".join(case_summary) + "\n")

        if is_root_case:
            with open(py_path, "r", encoding="utf-8") as f_in, open("output_program.py", "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())

            resumen = []
            resumen.append(f"[source] {src_path}")
            resumen.append(f"[ir] artifacts/{base}/5_ir.txt")
            resumen.append("[python] output_program.py")
            resumen.append(f"[returncode] {result.returncode}")
            if result.stdout:
                resumen.append("\n[stdout]\n" + result.stdout.strip())
            if result.stderr:
                resumen.append("\n[stderr]\n" + result.stderr.strip())
            with open("output.txt", "w", encoding="utf-8") as f_out:
                f_out.write("\n".join(resumen) + "\n")

        return 0 if result.returncode == 0 else 1

    except Exception as e:
        msg = f"[RUNTIME] {e}"
        write_artifact(outdir, "ERROR_runtime.txt", msg)
        write_artifact(outdir, "output.txt",
                       f"[source] {src_path}\n[status] error\n[type] runtime\n[msg] {e}\n")
        if is_root_case:
            with open("output.txt", "w", encoding="utf-8") as f_out:
                f_out.write(f"[source] {src_path}\n[RUNTIME ERROR] {e}\n")
        return 1

# ==========================
# Helpers de impresión EN CONSOLA
# ==========================

def _print_case_artifacts(outdir: str, is_root_case: bool):
    """Imprime las fases del caso actual; ROOT_* solo si es el caso input.txt."""
    def cat(filepath, title=None):
        if os.path.exists(filepath):
            print(f"\n=== {title or os.path.basename(filepath)} ===")
            with open(filepath, "r", encoding="utf-8") as f:
                print(f.read(), end="")

    ordered = [
        "1_tokens.txt",
        "2_parse_tree.txt",
        "3_ast.txt",
        "4_symbols.txt",
        "5_ir.txt",
        "6_output_program.py",
        "7_stdout.txt",
        "7_stderr.txt",
        "output.txt",
    ]
    for name in ordered:
        cat(os.path.join(outdir, name), title=name)

    # Solo imprimir ROOT_* si el caso actual ES input.txt
    if is_root_case:
        if os.path.exists("output_program.py"):
            cat("output_program.py", title="ROOT_output_program.py")
        if os.path.exists("output.txt"):
            cat("output.txt", title="ROOT_output.txt")

def _print_human_error(outdir: str):
    """Muestra el archivo de error más relevante con una interpretación clara."""
    err_lexsyn = os.path.join(outdir, "ERROR_lex_syn.txt")
    err_sem    = os.path.join(outdir, "ERROR_semantic.txt")
    err_run    = os.path.join(outdir, "ERROR_runtime.txt")

    if os.path.exists(err_lexsyn):
        print("\n=== ERROR LÉXICO/SINTÁCTICO ===")
        with open(err_lexsyn, "r", encoding="utf-8") as f:
            print(f.read(), end="")
        print("\nInterpretación: token/caracter inválido o estructura que no coincide con la gramática "
              "(falta ';', paréntesis sin cerrar, comparador inválido, keyword mal escrita, etc.).")
        return

    if os.path.exists(err_sem):
        print("\n=== ERROR SEMÁNTICO ===")
        with open(err_sem, "r", encoding="utf-8") as f:
            print(f.read(), end="")
        print("\nInterpretación: reglas violadas (variable no declarada, división por cero literal, "
              "print de variable inexistente, condición con ID no definido, etc.).")
        return

    if os.path.exists(err_run):
        print("\n=== ERROR EN TIEMPO DE EJECUCIÓN (PYTHON GENERADO) ===")
        with open(err_run, "r", encoding="utf-8") as f:
            print(f.read(), end="")
        print("\nInterpretación: el script Python generado arrojó una excepción al ejecutarse.")
        return

# ==========================
# Punto de entrada
# ==========================

def main():
    ap = argparse.ArgumentParser(description="Mini-compiler (gramatica → Python)")
    ap.add_argument("--src", required=False, default="input.txt",
                    help="ruta del archivo .txt del lenguaje; por defecto usa ./input.txt")
    # Aceptamos --quiet para compatibilidad con run_tests.py (silencia la consola)
    ap.add_argument("--quiet", action="store_true",
                    help="no imprimir las fases/errores en consola (solo artefactos)")
    args = ap.parse_args()

    if not os.path.exists(args.src):
        print(f"[ERROR] No existe el archivo: {args.src}")
        print("Crea un 'input.txt' en la raíz o especifica --src tests/valid/V1.txt, etc.")
        sys.exit(1)

    rc = compile_one(args.src)

    # Determinar si el caso actual es input.txt (para ROOT_*)
    is_root_case = (os.path.basename(args.src) == "input.txt") or (
        os.path.abspath(args.src) == os.path.abspath("input.txt")
    )

    # Si no está en modo quiet, mostramos salida pedagógica
    if not args.quiet:
        base = pathlib.Path(args.src).stem
        outdir = os.path.join("artifacts", base)
        if rc == 0:
            print("[OK] Compilación exitosa. Mostrando artefactos y salida:")
            _print_case_artifacts(outdir, is_root_case)
        else:
            print("[ERROR] El compilador detectó un problema. Detalle y explicación:")
            _print_human_error(outdir)
            _print_case_artifacts(outdir, is_root_case)

    sys.exit(rc)

if __name__ == "__main__":
    main()
