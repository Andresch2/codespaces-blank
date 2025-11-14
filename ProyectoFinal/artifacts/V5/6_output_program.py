base = 90000
horas_extra = (15000 * 1.2)
bono = (30000 / 1.5)
ingreso = ((base + horas_extra) + bono)
impuesto = 0
if ingreso > 200000:
    impuesto = (impuesto + ((ingreso - 200000) * 0.22))
if ingreso > 100000:
    impuesto = (impuesto + (100000 * 0.18))
print(impuesto)
