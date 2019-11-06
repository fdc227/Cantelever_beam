from sympy import *
from sympy.solvers.solveset import linear_coeffs
import pickle
from multiprocessing.pool import Pool

T_raw = open('T_final.pkl', 'rb')
T = pickle.load(T_raw)

############################################
######## STANDARD VARIABLE GEN FORM ########
############################################

var_raw = open('variable_list_str.pkl', 'rb')
variable_list_str = pickle.load(var_raw)
var_list_str, parameter_list_str = variable_list_str[0], variable_list_str[1]

parameter_list = []
for i in parameter_list_str:
    globals()[i] = symbols(i)

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
#############################################
#############################################

def T_eq_to_matrix(i):
    eq = T[i]
    print(f'Now seperating {i+1}/{len(T)}th row')
    arg_list = linear_coeffs(eq, *var_list_dt_dt)
    b = arg_list.pop()
    A = arg_list
    return A, b


p = Pool(len(T))
R_T = [r for r in range(len(T))]
T_lp = p.map(T_eq_to_matrix, R_T)

# print(T_lp)

A_list = []
b_list = []
for term in T_lp:
    A_list.append(term[0])
    b_list.append(term[1])
print(A_list)


A_raw = open('A.pkl', 'wb')
b_raw = open('b.pkl', 'wb')
pickle.dump(A_list, A_raw)
pickle.dump(b_list, b_raw)
