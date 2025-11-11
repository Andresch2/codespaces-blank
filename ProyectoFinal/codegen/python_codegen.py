# -*- coding: utf-8 -*-
# Traduce IR a script Python ejecutable

from codegen.ir import IRProgram, IRAssign, IRIfAssign, IRPrint

class PythonCodegen:
    def emit(self, ir: IRProgram) -> str:
        lines = []
        for ins in ir.instructions:
            if isinstance(ins, IRAssign):
                lines.append(f"{ins.name} = {ins.expr_py}")
            elif isinstance(ins, IRIfAssign):
                lines.append(f"if {ins.var} {ins.op} {ins.rhs_py}:")
                lines.append(f"    {ins.target} = {ins.value_py}")
            elif isinstance(ins, IRPrint):
                lines.append(f"print({ins.name})")
            else:
                raise RuntimeError("Instrucción IR no soportada")
        return "\n".join(lines) + "\n"
