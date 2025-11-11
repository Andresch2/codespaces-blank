# -*- coding: utf-8 -*-
# Implementación simple de tabla de símbolos (alcance global)

class SymbolTable:
    def __init__(self):
        self.defined = set()

    def define(self, name: str):
        self.defined.add(name)

    def is_defined(self, name: str) -> bool:
        return name in self.defined

    def dump(self) -> str:
        if not self.defined:
            return "(sin símbolos)"
        return "\n".join(sorted(self.defined))
