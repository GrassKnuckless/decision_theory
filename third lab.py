import tkinter as tk
import texttable as tt
from itertools import permutations

def label(label):
    return tk.Label(text=label, bd=5, font=("Courier", 15, "italic", "bold"), borderwidth=3, relief="solid")

def button_Borda(method, data):
    return tk.Button(text=method, bd=7, font=("Courier", 15, "italic", "bold"), bg='blue', command=lambda : press_button_Borda(data))
def button_Condorce(method, data):
    return tk.Button(text=method, bd=7, font=("Courier", 15, "italic", "bold"), bg='blue', command=lambda : press_button_Condorce(data))

def Clear():
    textbox.delete("1.0","end")

def press_button_Borda(data):
    textbox.configure(state='normal')
    Clear()
    
    table = tt.Texttable()
    data_table = [[]]
    head = ['A', 'B', 'C']
    put_in = []
    for el in head:
        put_in.append(BORDA(data, el))
    data_table.append(put_in)
    
    res_Borda = max(put_in)
    index_Borda = head[put_in.index(res_Borda)]
    
    align = []
    for i in range(0, len(head)):
        align.append('c')    
    
    table.add_rows(data_table)
    table.set_cols_align(align)
    table.header(head)
    textbox.insert('insert', "Метод Борда:\n")
    textbox.insert('insert', table.draw())
    textbox.insert('insert', '\nПереможцем за методом Борда є кандидат ' +
                   index_Borda + ' з рахунком ' + str(res_Borda))
    textbox.configure(state='disabled')
    
def BORDA(mat, cand):
    Sum = 0
    for i in range(0, len(mat)):    
        for j in range(0, len(mat[0])):
            if mat[i][j] == cand:
                if mat[i].index(cand) == 1:
                    Sum += mat[i][0] * 2
                elif mat[i].index(cand) == 2:
                    Sum += mat[i][0] * 1
                elif mat[i].index(cand) == 3:
                    Sum += mat[i][0] * 0
    return Sum

def press_button_Condorce(data):
    textbox.configure(state='normal')
    Clear()
    
    table = tt.Texttable()
    
    first = method_Condorce(data,'A', 'B')
    first_max = max(first)
    if first.index(first_max) == 0:
        str1 = 'A > B'
    else:
        str1 = 'B > A'
    
    second = method_Condorce(data, 'B', 'C')
    second_max = max(second)
    if second.index(second_max) == 0:
        str2 = 'B > C'
    else:
        str2 = 'C > B'
    
    third = method_Condorce(data, 'A', 'C')
    third_max = max(third)
    if third.index(third_max) == 0:
        str3 = 'A > C'
    else:
        str3 = 'C > A'

    table_data = [["A > B\nB > A", str(first[0]) + "\n" + str(first[1]), str1],
                  ["B > C\nC > B", str(second[0]) + "\n" + str(second[1]), str2],
                  ["A > C\nC > A", str(third[0]) + "\n" + str(third[1]), str3]]
    
    table.add_rows(table_data)
    textbox.insert('insert', "Метод Кондорсе:\n")
    textbox.insert('insert', table.draw())
    
    all_compare = [str1, str2, str3]
    all_compare = list(permutations(all_compare))
    for i in range(0, len(all_compare)):
        compare(all_compare[i][0], all_compare[i][1], all_compare[i][2])
    
    textbox.configure(state='disabled')
    
def method_Condorce(mat, left, right):
    res = list()
    res1 = 0
    res2 = 0
    for i in range(0, len(mat)):
        if mat[i].index(left) < mat[i].index(right):
            res1 += mat[i][0]
        else:
            res2 += mat[i][0]
    res.append(res1)
    res.append(res2)
    return res

def compare(str1, str2, str3):
    if str1[len(str1) - 1] == str2[0]:
        str1_str2 = str1 + ' > ' + str2[len(str2) - 1]
        if str1_str2[0] == str3[0] and str1_str2[len(str1_str2) - 1] == str3[len(str3) - 1]:
            textbox.insert('insert', "\n" + str(str1_str2))
            textbox.insert('insert', '\nПереможцем за методом Кондорсе є кандидат ' + str(str1_str2[0]))
        else:
            textbox.insert('insert', 'Разом ці твердження суперечливі. Неможливо прийняти якесь узгоджене рішення')

main_window = tk.Tk()
main_window.geometry("980x450")
main_window.resizable(0,0)
main_window.title('Методи колективних рішень')

matrix = []

with open('3.txt', 'r') as file:
    for line in file:
            strip = line.strip()
            split = strip.split(' ')
            for i in range(0, len(split)):
                if split[i].isdigit():
                    split[i] = int(split[i])
            matrix.append(split)

amount_of_voters = ""
benefits = ""
for i in range(0, len(matrix)):
    amount_of_voters += str(matrix[i][0])
    amount_of_voters += "\n"
    for j in range(1, len(matrix[i])):
        benefits += matrix[i][j]
        if j != len(matrix[i])-1:
            benefits += " - > "
    benefits += "\n"
amount_of_voters = amount_of_voters[:-1]
benefits = benefits[:-1]


label("Число виборців та їх переваги:").grid(row=1, column=1, columnspan=4, stick='wens', padx=3, pady=3)
label(amount_of_voters).grid(row=2, rowspan=3, column=1, stick='wens', padx=3, pady=3)
label(benefits).grid(row=2, rowspan=3, column=2, columnspan=3, stick='wens', padx=3, pady=3)

button_Borda("Метод Борда", matrix).grid(row=5, column=1, columnspan=4, stick='wens', padx=3, pady=3)
button_Condorce("Метод Кондорсе", matrix).grid(row=6, column=1, columnspan=4, stick='wens', padx=3, pady=3)

label("Вивід результатів:").grid(row=1, column=5, columnspan=6, stick='wens', padx=3, pady=3)
textbox = tk.Text(main_window, heigh=14, width=45, state='disabled', font=("Courier", 14, "italic", "bold"))
textbox.grid(row=2, rowspan=5, column=5, columnspan=6, stick='wens', padx=3, pady=3)

for i in range(0, 10):
    main_window.grid_columnconfigure(i, minsize = 50)

for i in range(0, 7):
    main_window.grid_rowconfigure(i, minsize = 50)

main_window.mainloop()





