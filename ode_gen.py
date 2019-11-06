from sympy import *
import numpy as np
import pickle

########### VARIABLE GEN ############
var_raw = open('variable_list_str.pkl', 'rb')
variable_list_str = pickle.load(var_raw)
var_list_str, parameter_list_str = variable_list_str[0], variable_list_str[1]
parameter_list = []
for i in parameter_list_str:
    globals()[i] = symbols(i)
    parameter_list.append(globals()[i])
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
#####################################

A_raw = open('A.pkl', 'rb')
A = pickle.load(A_raw)
b_raw = open('b.pkl', 'rb')
b = pickle.load(b_raw)
U_raw = open('U_raw.pkl', 'rb')
U = pickle.load(U_raw)
W_raw = open('W_final.pkl', 'rb')
W = pickle.load(W_raw)
IC_raw = open('IC.pkl', 'rb')
IC_list = pickle.load(IC_raw)
q_IC, parameter_IC = IC_list[0], IC_list[1]



