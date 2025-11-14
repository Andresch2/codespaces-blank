sueldo = ((80000 + 20000) * 1.05)
extras = ((12000 * 1.3) + (3500 / 1.4))
ingreso = (sueldo + extras)
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
