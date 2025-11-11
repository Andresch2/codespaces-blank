base = 110000
extra = 15000
tasa = 0.18
ingreso = (base + extra)
impuesto = 0
if ingreso >= 120000:
    impuesto = (ingreso * tasa)
print(impuesto)
