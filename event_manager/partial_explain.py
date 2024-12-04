from functools import partial


def f(a, b):
    print(a, b)


# Partielle Funktion mit Wert a=3 anlegen
pf = partial(f, a=3)

# Vollständiger Funktionsaufruf von f
pf(b=4)
