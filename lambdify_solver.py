from sympy import *
import pickle
import numpy
from numpy.linalg import inv
from scipy.integrate import odeint

A_raw = open('A.pkl', 'rb')
A_list = pickle.load(A_raw)
b_raw = open('b.pkl', 'rb')
b_list = pickle.load(b_raw)
U_raw = open('U_final.pkl', 'rb')
U_list = pickle.load(U_raw)

IC_raw = open('IC.pkl', 'rb')
IC = pickle.load(IC_raw)

q_IC, parameter_IC = IC[0], IC[1]
parameter_IC = numpy.array(parameter_IC, dtype=numpy.float64)

############################################
######## STANDARD VARIABLE GEN FORM ########
############################################

var_raw = open('variable_list_str.pkl', 'rb')
variable_list_str = pickle.load(var_raw)
var_list_str, parameter_list_str = variable_list_str[0], variable_list_str[1]

parameter_list = []
for i in parameter_list_str:
    globals()[i] = symbols(i)
    parameter_list.append(globals()[i])
# print(parameter_list)

var_list = []
for i in var_list_str:
    j = i[0:-3]
    globals()[j] = symbols(j)
    var_list.append(globals()[j])
var_list_dt = []
for i in var_list_str:
    j = i[0:-3] +'_dt'
    globals()[j] = symbols(j)
    var_list_dt.append(globals()[j])
var_list_dt_dt = []
for i in var_list_str:
    j = i[0:-3] +'_dt_dt'
    globals()[j] = symbols(j)
    var_list_dt_dt.append(globals()[j])

#############################################
##################  END  ####################
#############################################

param_subs = {}
for i in range(len(parameter_list)):
    param_subs[parameter_list[i]] = parameter_IC[i]

A_list = (Matrix(A_list).subs(param_subs)).tolist()
b_list = (Matrix(b_list).subs(param_subs)).tolist()
U_list = (Matrix(U_list).subs(param_subs)).tolist()

A_f = lambdify([*var_list, *var_list_dt], A_list)
b_f = lambdify([*var_list, *var_list_dt], b_list)
U_f = lambdify([*var_list, *var_list_dt], U_list)

q_IC_np = numpy.array(q_IC, dtype=numpy.float64)
IC_len = len(q_IC)

def equation_ode(y, t):
    A_m = A_f(*y)
    b_m = numpy.array(b_f(*y)).flatten()
    U_m = numpy.array(U_f(*y)).flatten()
    RHS = -b_m - U_m
    output_0 = y[IC_len // 2 : IC_len]
    output_1 = numpy.array(numpy.dot(inv(A_m), RHS), dtype=numpy.float64)
    output = numpy.concatenate((output_0, output_1), axis=0)
    print(y)
    return  output

t = numpy.linspace(0, 10, 101)
sol = odeint(equation_ode, q_IC_np, t)

sol_raw = open('sol.pkl', 'wb')
pickle.dump(sol, sol_raw)
