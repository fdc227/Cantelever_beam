from sympy import *
import pickle
from shape_gen import shape_gen
from torsion_shape_gen import torsion_shape_gen

# 'it is recommended that you not use I, E, S, N, C, O, or Q for variable or symbol names, as those are used for the imaginary unit (i), 
# the base of the natural logarithm (e), the sympify() function (see Symbolic Expressions below), 
# numeric evaluation (N() is equivalent to evalf() ), the big O order symbol (as in O(nlogn)), 
# and the assumptions object that holds a list of supported ask keys (such as Q.real), respectively.'
# copied from https://docs.sympy.org/latest/gotchas.html

###############################################
###########     USER DEFINITION      ##########
###############################################

##### Put variables as a list of strings ######

var_list_str = []
parameter_list_str = ['L', 'EE', 'II', 'rho', 'A', 'm', 'G', 'J', 'x_f', 'V_inf', 'e', 'M_theta']
others = ['y']

########## DEFINE VARIABLE STRINGS ############

q_bending = []
q_bending_dot = []
q_torsion = []
q_inplane = []
q_inplane_dot = []

for i in range(1, 11):
    q_bending.append(f'q{i}_b')
    q_bending_dot.append(f'q{i}_b_dot')
    q_torsion.append(f'q{i}_t')
    q_inplane.append(f'q{i}_i')
    q_inplane_dot.append(f'q{i}_i_dot')

var_list_str = [*q_bending, *q_bending_dot, *q_torsion, *q_inplane, *q_inplane_dot]

delta_q_bending = []
delta_q_bending_dot = []
delta_q_torsion = []
delta_q_inplane = []
delta_q_inplane_dot = []

for i in range(1, 11):
    delta_q_bending.append(f'delta_q{i}_b')
    delta_q_bending_dot.append(f'delta_q{i}_b_dot')
    delta_q_torsion.append(f'delta_q{i}_t')
    delta_q_inplane.append(f'delta_q{i}_i')
    delta_q_inplane_dot.append(f'delta_q{i}_i_dot')

delta_var_list_str = [*delta_q_bending, *delta_q_bending_dot, *delta_q_torsion, *delta_q_inplane, *delta_q_inplane_dot]


############ Initial Conditions  ##############

IC = []
# Assuming r = 10cm = 0.1m
parameter_IC = [1.0, 10**6, 0.75*10**(-4), 1,225, 3.14*10**(-2), 6.0, 3.75*10**6, 0.75*10**(-4), 0.5, 10, 0.3, 0.3]

q_IC = []
for i in range(10):
    q_IC.append((i+1)*0.2)
for i in range(10):
    q_IC.append(0.2)
for i in range(10):
    q_IC.append((i+1)*0.2)
for i in range(10):
    q_IC.append((i+1)*0.2)
for i in range(10):
    q_IC.append(0.2)
for i in range(50):
    q_IC.append(0)

IC = [q_IC, parameter_IC]

###############################################

##### Express the kinetic and potential energy in terms of strings in sympy form #####
##### If expressions appear in terms of repeating patterns, write one single expression and a list of variables upon which the pattern will be applied ######
##### use 'diff(q, t)' to express the first order derivative of variable 'q' #####

x, y = symbols('x, y')
L = symbols('L')
shapes = shape_gen(4)
beam_shapes = []
for term in shapes:
    new_term = term.subs({x:y})
    beam_shapes.append(new_term)
torsion_shapes = torsion_shape_gen()

k1, k2, k3, k4 = symbols('k1, k2, k3, k4') # Symbols for positional-identification
k5, k6, k7, k8, k9, p0 = symbols('k5, k6, k7, k8, k9, p0')
p1, p2, p3, p4, p5, p6 = symbols('p1, p2, p3, p4, p5, p6')

fb = beam_shapes[0]*k1 + beam_shapes[1]*k2 + beam_shapes[2]*k3 + beam_shapes[3]*k4
ft = torsion_shapes[0]*k5 + torsion_shapes[1]*k6
fi = beam_shapes[0]*k7 + beam_shapes[1]*k8 + beam_shapes[2]*k9 + beam_shapes[3]*p0
delta_fb = beam_shapes[0]*p1 + beam_shapes[1]*p2 + beam_shapes[2]*p3 + beam_shapes[3]*p4
delta_ft = torsion_shapes[0]*p5 + torsion_shapes[1]*p6

T_func_f_format = f'Integral(1/2*m*(c-2*c*x_f)*Derivative({ft},(t,2))**2 + 1/2*m*(Derivative({fb},(t,2))**2+Derivative({fi},(t,2))**2), (y, 0, L))'
U_func_f_format = f'Integral(1/2*EE*II*(Derivative({fb},(y,2))**2+Derivative({fi},(y,2))**2) + 1/2*G*J*Derivative({ft},y)**2, (y, 0, L))'
alpha = f'Derivative({fb},t)/(V_inf)+({ft})'
dL = f'1/2*rho*V_inf**2*(2*3.14)*({alpha})'
dM = f'1/2*rho*V_inf**2*(e*(2*3.14)+M_theta*1/4*(1/V_inf)*Derivative({ft},t))'
W_func_f_format = f'Integral(({dL})*({delta_fb})+({dM})*({delta_ft}), (y, 0, L))'

q_bending_T = q_bending.copy()
q_bending_T.insert(0, '0')
q_bending_dot_T = q_bending_dot.copy()
q_bending_dot_T.insert(0, '0')
q_torsion_T = q_torsion.copy()
q_torsion_T.insert(0, '0')
q_inplane_T = q_inplane.copy()
q_inplane_T.insert(0, '0')
q_inplane_dot_T = q_inplane_dot.copy()
q_inplane_dot_T.insert(0, '0')
print(q_bending_T)

delta_q_bending_T = delta_q_bending.copy()
delta_q_bending_T.insert(0, '0')
delta_q_bending_dot_T = delta_q_bending_dot.copy()
delta_q_bending_dot_T.insert(0, '0')
delta_q_torsion_T = delta_q_torsion.copy()
delta_q_torsion_T.insert(0, '0')
delta_q_inplane_T = delta_q_inplane.copy()
delta_q_inplane_T.insert(0, '0')
delta_q_inplane_dot_T = delta_q_inplane_dot.copy()
delta_q_inplane_dot_T.insert(0, '0')
print(delta_q_bending_T)

T = [[T_func_f_format, {'k1':q_bending_T[0:10], 'k2':q_bending_dot_T[0:10], 'k3':q_bending_T[1:11], 'k4':q_bending_dot_T[1:11], 'k5':q_torsion_T[0:10], 'k6':q_torsion_T[1:11], 'k7':q_inplane_T[0:10], 'k8':q_inplane_dot_T[0:10], 'k9':q_inplane_T[1:11], 'p0':q_inplane_dot_T[1:11]}]]
U = [[U_func_f_format, {'k1':q_bending_T[0:10], 'k2':q_bending_dot_T[0:10], 'k3':q_bending_T[1:11], 'k4':q_bending_dot_T[1:11], 'k5':q_torsion_T[0:10], 'k6':q_torsion_T[1:11], 'k7':q_inplane_T[0:10], 'k8':q_inplane_dot_T[0:10], 'k9':q_inplane_T[1:11], 'p0':q_inplane_dot_T[1:11]}]]
W = [[W_func_f_format, {'k1':q_bending_T[0:10], 'k2':q_bending_dot_T[0:10], 'k3':q_bending_T[1:11], 'k4':q_bending_dot_T[1:11], 'k5':q_torsion_T[0:10], 'k6':q_torsion_T[1:11], 'k7':q_inplane_T[0:10], 'k8':q_inplane_dot_T[0:10], 'k9':q_inplane_T[1:11], 'p0':q_inplane_dot_T[1:11], 
                        'p1':delta_q_bending_T[0:10], 'p2':delta_q_bending_dot_T[0:10], 'p3':delta_q_bending_T[1:11], 'p4':delta_q_bending_dot_T[1:11], 'p5':delta_q_torsion_T[0:10], 'p6':delta_q_torsion_T[1:11]}]]

###############################################
##########   USER DEFINITION END   ############
###############################################

variable_list_str = [var_list_str, parameter_list_str, others]
var_raw = open('variable_list_str.pkl', 'wb')
pickle.dump(variable_list_str, var_raw)
T_raw = open('T_raw.pkl', 'wb')
pickle.dump(T, T_raw)
U_raw = open('U_raw.pkl', 'wb')
pickle.dump(U, U_raw)
IC_raw = open('IC.pkl', 'wb')
pickle.dump(IC, IC_raw)
delta_data = [delta_var_list_str, W]
delta_raw = open('delta_raw.pkl', 'wb')
pickle.dump(delta_data, delta_raw)