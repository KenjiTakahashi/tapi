# -*- coding: utf-8 -*-

def dzieli(a, b):
    try:
        return a % b == 0
    except ZeroDivisionError:
        return False

def cyfry(a):
    return sum(map(int, str(a)))

def iloczyn(a):
    return reduce(lambda x, y: x * y, map(int ,str(a)))

def fajna(a):
    return dzieli(a, cyfry(a)) and dzieli(a, iloczyn(a))

def lista_fajnych(n):
    return filter(fajna, range(1, n))

print(lista_fajnych(120))
