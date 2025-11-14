sueldo = 140000.5
bonos = ((23000 * 1.15) - (1500 / 3))
deduc = (3200.25 / 1.5)
ingreso = ((sueldo + bonos) - deduc)
t1 = 0.18
t2 = 0.22
t3 = 0.3
impuesto = 0
if ingreso > 300000:
    impuesto = (impuesto + ((ingreso - 300000) * t3))
if ingreso > 200000:
    impuesto = (impuesto + (100000 * t2))
if ingreso > 200000:
    impuesto = (impuesto + (100000 * t1))
if ingreso <= 200000:
    impuesto = (impuesto + ((ingreso - 100000) * t1))
print(impuesto)
