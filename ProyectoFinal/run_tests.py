# -*- coding: utf-8 -*-
# Ejecuta todos los tests de tests/valid y tests/invalid
import glob, subprocess, sys

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

def run_all():
    ok_total = 0
    fail_total = 0
    details = []

    # válidos
    for path in sorted(glob.glob("tests/valid/*.txt")):
        exp = expected(path)  # debe ser "ok"
        res = subprocess.run([sys.executable, "main.py", "--src", path])
        passed = (res.returncode == 0 and exp == "ok")
        ok_total += 1 if passed else 0
        fail_total += 0 if passed else 1
        details.append((path, "OK" if passed else "FAIL (debía OK)"))

    # inválidos
    for path in sorted(glob.glob("tests/invalid/*.txt")):
        exp = expected(path)  # lex|syn|sem
        res = subprocess.run([sys.executable, "main.py", "--src", path])
        passed = (res.returncode != 0 and exp in ("lex","syn","sem"))
        ok_total += 1 if passed else 0
        fail_total += 0 if passed else 1
        details.append((path, "OK" if passed else f"FAIL (debía fallo {exp})"))

    print("==== RESUMEN ====")
    for p, s in details:
        print(f"{p}: {s}")
    print(f"Correctos: {ok_total}  |  Incorrectos: {fail_total}")
    return 0 if fail_total == 0 else 1

if __name__ == "__main__":
    sys.exit(run_all())
