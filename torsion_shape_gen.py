from sympy import *

def torsion_shape_gen():
    y, L = symbols('y, L')
    return [1 - y/L, y/L]

if __name__ == "__main__":
    print(torsion_shape_gen())