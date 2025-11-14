# -*- coding: utf-8 -*-
# Ejecuta todos los tests en silencio y muestra el tipo de error detectado
import glob, subprocess, sys, os, pathlib

def expected(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                ls = line.strip()
                if ls.startswith("// @expect:"):
                    return ls.split(":",1)[1].strip()
                if ls == "" or not ls.startswith("//"):
                    break
    except:
        pass
    return "ok"

def observed_error(case_path):
    """Inspecciona artifacts/<CASO>/ para inferir el tipo de error."""
    stem = pathlib.Path(case_path).stem
    outdir = os.path.join("artifacts", stem)
    if os.path.exists(os.path.join(outdir, "ERROR_semantic.txt")):
        return "sem"
    if os.path.exists(os.path.join(outdir, "ERROR_lex_syn.txt")):
        return "lex/syn"
    # opcional: si hubiera error de ejecución
    if os.path.exists(os.path.join(outdir, "ERROR_runtime.txt")):
        return "runtime"
    return "ok"

def run_all():
    ok_total = 0
    fail_total = 0
    details = []

    # válidos
    for path in sorted(glob.glob("tests/valid/*.txt")):
        exp = expected(path)  # "ok"
        res = subprocess.run(
            [sys.executable, "main.py", "--quiet", "--src", path],
            capture_output=True, text=True
        )
        obs = observed_error(path)
        passed = (res.returncode == 0 and exp == "ok" and obs == "ok")
        ok_total += 1 if passed else 0
        fail_total += 0 if passed else 1
        details.append((path, "OK" if passed else f"FAIL (debía OK, obs={obs})"))

    # inválidos
    for path in sorted(glob.glob("tests/invalid/*.txt")):
        exp = expected(path)  # "lex" | "syn" | "sem"
        res = subprocess.run(
            [sys.executable, "main.py", "--quiet", "--src", path],
            capture_output=True, text=True
        )
        obs = observed_error(path)
        # normalizo: nuestro compilador no separa lex vs syn en archivos distintos
        exp_norm = "lex/syn" if exp in ("lex", "syn") else exp
        passed = (res.returncode != 0 and obs == exp_norm)
        status = "OK" if passed else f"FAIL (debía {exp}, obs={obs})"
        ok_total += 1 if passed else 0
        fail_total += 0 if passed else 1
        details.append((path, f"{status}"))

    print("==== RESUMEN ====")
    for p, s in details:
        print(f"{p}: {s}")
    print(f"Correctos: {ok_total}  |  Incorrectos: {fail_total}")
    return 0 if fail_total == 0 else 1

if __name__ == "__main__":
    sys.exit(run_all())
