base = 98765
product = ((43210 * 1.35) - (1250 / 2.5))
horas = ((37 * 4500) / 1.1)
bono1 = (base * 0.07)
bono2 = (product * 0.045)
ajuste = ((1 + (3 / 100)) + (2 / 100))
ingreso = (((((base + product) + horas) + bono1) + bono2) * ajuste)
t1 = ((1 / 5) - (1 / 20))
t2 = 0.21
t3 = ((7 / 25) + (1 / 100))
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
