import numpy as np
import texttable as tt
from pulp import *
    
def print_unknown(mat, sign, unknown, function, known):
    print("Система рівнянь:")
    for i in range(0, len(mat)):
        print(str(sum(mat[i] * unknown)) + " " + sign + " 1")
        
    table_unknown = tt.Texttable()
    cols_align = []
    
    print("Функція:")
    if sign == ">=":
        print("F(x) = " + str(sum(unknown)) + " -> Min")
        cols_header = unknown+["F(x)"]
    elif sign == "<=":
        print("F(y) = " + str(sum(unknown)) + " -> Max")
        cols_header = unknown+["F(y)"]
    table_unknown.header(cols_header)
    
    print("Розв'язок:")
    for i in range(0, len(cols_header)):
        cols_align.append('c')
    table_unknown.add_row(known+[function])
    table_unknown.set_cols_align(cols_align)
    print(table_unknown.draw())

def print_pesults(cost, probability, p_or_q):
    table_unknown = tt.Texttable()
    cols_align = []
    cols_width = []
    cols_dtype = []
    cols_header = []
    
    probability = [round(num, 8) for num in probability]
    cost = round(cost, 8)
    
    if p_or_q == "p":
        for i in range(0, len(probability)):
            cols_header.append(p_or_q + str(i+1))
    elif p_or_q == "q":
        for i in range(0, len(probability)):
            cols_header.append(p_or_q + str(i+1))    
    cols_header.append("Ціна гри:")
    table_unknown.header(cols_header)
    
    for i in range(0, len(cols_header)):
        cols_align.append('c')
        cols_width.append(11)
        cols_dtype.append('t')
    table_unknown.set_cols_dtype(cols_dtype)
    table_unknown.add_row(probability+[cost])
    table_unknown.set_cols_align(cols_align)
    table_unknown.set_cols_width(cols_width)
    print(table_unknown.draw())
        
input_matrix = np.loadtxt("5.txt", dtype=int)
    
transpose_new_matrix = np.transpose(input_matrix)
    
x = []
for i in range(0, len(transpose_new_matrix[0])):
    x.append(LpVariable("x" + str(i + 1), lowBound=0))
problem_x = LpProblem("Simple Problem", LpMinimize)     
    
problem_x += sum(x)

for i in range(0, len(transpose_new_matrix)):
    problem_x += sum(transpose_new_matrix[i]*x) >= 1
    
problem_x.solve()
X = []
for variable in problem_x.variables():
    X.append(variable.varValue)
F_x = value(problem_x.objective)

print("Стратегія для А:")
print_unknown(transpose_new_matrix, ">=", x, F_x, X)
print()
      
V_x = 1 / sum(X)
p = []
for element in X:
    p.append(element * V_x)

print("Ціна гри і ймовірності застосування стратегій гравця А:")
print_pesults(V_x, p, "p")
print()
    

y = []
for i in range(0, len(input_matrix[0])):
    y.append(LpVariable("y" + str(i + 1), lowBound=0))
problem_y = LpProblem("Simple Problem", LpMaximize)        
    
problem_y += sum(y)
 
for i in range(0, len(input_matrix)):
    problem_y += sum(input_matrix[i]*y) <= 1

problem_y.solve()
Y = []
for variable in problem_y.variables():
    Y.append(variable.varValue)
F_y = value(problem_y.objective)
    
print("Стратегія для B:")
print_unknown(input_matrix, "<=", y, F_y, Y)
print()
    
V_y = 1 / sum(Y)
q = []
for element in Y:
    q.append(element * V_y)
        
print("Ціна гри і ймовірності застосування стратегій гравця B:")
print_pesults(V_y, q, "q")
print()