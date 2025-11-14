bruto = (80000 + 95000)
ajuste = ((1.02 + 0.03) + 0.02)
ingreso = (bruto * ajuste)
t1 = 0.18
t2 = 0.22
impuesto = 0
if ingreso > 200000:
    impuesto = (impuesto + ((ingreso - 200000) * t2))
if ingreso > 200000:
    impuesto = (impuesto + (100000 * t1))
if ingreso <= 200000:
    impuesto = (impuesto + ((ingreso - 100000) * t1))
print(impuesto)
