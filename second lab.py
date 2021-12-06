import texttable as tt

def year_5_cal(mat, year):
    earn = year * mat[1]
    waste = year * mat[3]
    win = earn * mat[2] + waste * mat[4] - mat[0]
    return earn, waste, win

def year_4_cal(mat1, mat2, year):
    earn = year * mat1[1]
    waste = year * mat1[3]
    win = earn * mat2[2] + waste * mat2[3] - mat1[0]
    return earn, waste, win

def print_5_year(mat, income, waste, win, strategy):
    tableA = tt.Texttable()
    mat.append(income)
    mat.append(waste)
    mat.append(win)
    
    head = []
    if strategy == 'A':
        head = ['M1', 'D1', 'P1', 'D2', 'P2', 'Дохід за 5 років',
                'Витрати за 5 років', 'Середній виграш стратегії A']
    elif strategy == 'B':
        head = ['M2', 'D1', 'P1', 'D2', 'P2', 'Дохід за 5 років',
                'Витрати за 5 років', 'Середній виграш стратегії B']
    
    align = []
    for i in range(0, len(head)):
        align.append('c')
    
    dataA = [[]]
    dataA.append(mat)
    tableA.add_rows(dataA)
    tableA.set_cols_align(align)
    tableA.header(head)
    print(tableA.draw())

def print_4_year(mat1, mat2, income, waste, win, strategy):
    tableA = tt.Texttable()
    mat1[2] = mat2[2]
    mat1[4] = mat2[3]
    mat1[5] = income
    mat1[6] = waste
    mat1[7] = win
    
    head = []
    if strategy == 'A':
        head = ['M1', 'D1', 'P1', 'D2', 'P2', 'Дохід за 4 років',
                'Витрати за 5 років', 'Середній виграш стратегії A']
    elif strategy == 'B':
        head = ['M2', 'D1', 'P1', 'D2', 'P2', 'Дохід за 4 років',
                'Витрати за 4 років', 'Середній виграш стратегії B']
    
    align = []
    for i in range(0, len(head)):
        align.append('c')
    
    dataA = [[]]
    dataA.append(mat1)
    tableA.add_rows(dataA)
    tableA.set_cols_align(align)
    tableA.header(head)
    print(tableA.draw())

with open('2.txt') as fd:
    for n, line in enumerate(fd):
        if n == 0:
            A = line.strip()
        elif n == 1:
            B = line.strip()
        elif n == 2:
            C = line.strip()
fd.close()

A = A.split(' ')
B = B.split(' ')
C = C.split(' ')

A = [float(i) for i in A]
B = [float(i) for i in B]
C = [float(i) for i in C]

incomeA, wasteA, win_A_for_5_years = year_5_cal(A, 5)
incomeB, wasteB, win_B_for_5_years = year_5_cal(B, 5)

incomeA1, wasteA1, win_A_for_4_years = year_4_cal(A, C, 4)
incomeB1, wasteB1, win_B_for_4_years = year_4_cal(B, C, 4)

if win_A_for_4_years > win_B_for_4_years:
    win_for_4_years = win_A_for_4_years
else:
    win_for_4_years = win_B_for_4_years
    
win_C1_for_4_years = C[0] * win_for_4_years
win_C2_for_4_years = C[1] * 0

if win_C1_for_4_years > win_C2_for_4_years:
    win_C_for_5_years = win_C1_for_4_years
else:
    win_C_for_5_years = win_C2_for_4_years

print("Стратегія A: ")
print_5_year(A, incomeA, wasteA, win_A_for_5_years, "A")
print("Стратегія B: ")
print_5_year(B, incomeB, wasteB, win_B_for_5_years, "B")
print("Стратегія C: ")
print_4_year(A, C, incomeA1, wasteA1, win_A_for_4_years, "A")
print_4_year(B, C, incomeB1, wasteB1, win_B_for_4_years, "B")

tableC = tt.Texttable()
dataC = [[]]
dataC.append([C[0], C[1], win_A_for_4_years, win_B_for_4_years, win_C1_for_4_years,
              win_C2_for_4_years, win_C_for_5_years])
tableC.add_rows(dataC)
tableC.set_cols_align(['c','c','c','c','c','c','c'])
tableC.header(['P3', 'P4', 'Виграш за 4 роки для A', 'Виграш за 4 роки для B',
               'Виграш за 5 років для C1', 'Виграш за 5 років для C2',
               'Виграш за 5 років для C'])
print(tableC.draw())

print("Табличка результатів для усіх стратегій:")
table = tt.Texttable()
data = [[]]
data.append([win_A_for_5_years, win_B_for_5_years, win_C_for_5_years])
table.add_rows(data)
table.set_cols_align(['c','c','c'])
table.header(['A', 'B', 'C'])
print(table.draw())

win_strategy = max(win_A_for_5_years, win_B_for_5_years, win_C_for_5_years)
if win_strategy == win_A_for_5_years:
    print('Стратегія виграшу – це А, тому що середній очікуваний виграш дорівнює ', win_strategy)
    print('Краще побудувати великий завод')
elif win_strategy == win_B_for_5_years:
    print('Стратегія виграшу – це B, тому що середній очікуваний виграш дорівнює ', win_strategy)
    print('Краще побудувати   завод')
elif win_strategy == win_C_for_5_years:
    print('Стратегія виграшу – це C, тому що середній очікуваний виграш дорівнює ', win_strategy)
    print('Краще відкласти будівництво на рік для збору додаткової інформації')