import numpy as np
from sympy import *

# ord_ = number of variables needed for each finite element

def shape_gen(ord_):
    # Constructing symbols for polynomial
    if ord_ / 2 - ord_ // 2 == 0:
        pass
    else:
        raise Exception("ord_ must be an non-negative even number")

    coeff = []
    L = symbols('L')
    for i in range(ord_):
        coeff.append('c' + f'{i}')
    x = symbols('x')
    coeffexpr = []
    for s in coeff:
        globals()[s] = symbols(s)
        coeffexpr.append(symbols(s))
    #print(coeff)
    #print(coeffexpr)

    # Construction for terms in y
    term = []
    e = 0
    while e < len(coeffexpr):
        term.append(coeffexpr[e] * x**e)
        e += 1
    #print(term)

    # Constructing y
    y = 0
    for t in term:
        y += t
    # print(y)
 

    n = ord_ // 2
    Q = []
    for i in range(n):
        k = diff(y, x, i)
        globals()['q'+f'{i}'] = k.subs(x, 0)
        Q.append(k.subs(x,0))
    for i in range(n, ord_):
        k = diff(y, x, i - n)
        globals()['q'+f'{i}'] = k.subs(x, L)
        Q.append(k.subs(x, L))

    # print(Q)
    # print(coeffexpr)
    
    A, b = linear_eq_to_matrix(Q, coeffexpr)
    # print(A)
    # print(b)

    shape_func = []

    A_ = A**-1
    # print(A_)

    for j in range(ord_):
        expr = 0
        for i in range(ord_):
            expr += A_[i, j] * x ** i
        shape_func.append(expr)

    # print(shape_func) 
    return shape_func
    

if __name__ == '__main__':
    shape_func = shape_gen(4)
    print(shape_func)