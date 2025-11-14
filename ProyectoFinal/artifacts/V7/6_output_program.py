a = 12345
b = 6789
c = 2.75
ingreso = (((a * (b + 111)) / (3 + c)) + ((a - b) * (c + 1.25)))
tasa = ((3 / 20) + (7 / 200))
impuesto = 0
if ingreso > 100000:
    impuesto = (ingreso * tasa)
print(impuesto)
