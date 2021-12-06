import tkinter as tk
import numpy as np
import texttable as tt
from statistics import mode

def button(method, data):
    return tk.Button(text=method, bd=7, font=("Courier", 15, "italic", "bold"), bg='blue', command=lambda : press_button(data, method))

def button_all(method, data):
    return tk.Button(text=method, bd=7, font=("Courier", 15, "italic", "bold"), bg='blue', command=lambda : press_button_all(data))

def label(label):
    return tk.Label(text=label, bd=5, font=("Courier", 15, "italic", "bold"), borderwidth=3, relief="solid")

def press_button(data, method):
    textbox.configure(state='normal')
    Clear()
    
    table = tt.Texttable()
    data_table = [[]]
    head = ['№', 'A1', 'A2', 'A3']
    
    res = []
    if method == "Метод Вальда":
        res = Wald(data)
        head.append(method)
    elif method == "Метод Максимуму":
        res = Max(data)
        head.append(method)
    elif method == "Метод Гурвіца":
        res = Hurwitz(data)
        head.append(method)
    elif method == "Метод Лапласа":
        res = Laplace(data)
        head.append(method)
    elif method == "Метод Байеса-Лапласа":
        res = Bayes_Laplace(data)
        head.append(method)

    for i in range(0, len(data)):
        put_in = []
        for j in range(0, len(data[i])):
            put_in.append(data[i][j])
        put_in.insert(0, i+1)
        put_in.append(res[i])
        data_table.append(put_in)
    
    align = []
    for i in range(0, len(head)):
        align.append('c')    
    
    table.add_rows(data_table)
    table.set_cols_align(align)
    table.header(head)
    textbox.insert('insert', table.draw())
    
    str1 = "\n Максимальне значення цього методу: " + str(max(res))
    textbox.insert('insert', str1)
    
    str2 = "\n Це стратегія №" + str(res.index(max(res))+1)
    textbox.insert('insert', str2)
    
    textbox.configure(state='disabled')    

def press_button_all(data):
    textbox.configure(state='normal')
    Clear()
    
    table = tt.Texttable()
    data_table = [[]]
    head = ['№', 'Матриця', 'Вальда', 'Максимуму', 'Гурвіца', 'Лапласа', 'Байеса-Лапласа']
    res_Wald = Wald(data)
    res_Max = Max(data)
    res_Hurwitz = Hurwitz(data)
    res_Laplace = Laplace(data)
    res_Bayes_Laplace = Bayes_Laplace(data)
    
    
    for i in range(0, len(data)):
        put_in = []
        put_in.append(i+1)
        put_in.append(data[i])
        put_in.append(res_Wald[i])
        put_in.append(res_Max[i])
        put_in.append(res_Hurwitz[i])
        put_in.append(res_Laplace[i])
        put_in.append(res_Bayes_Laplace[i])
        data_table.append(put_in)
    data_table.append([4, "Максимальні значення:", max(res_Wald), max(res_Max),
                       max(res_Hurwitz), max(res_Laplace), max(res_Bayes_Laplace)])
    
    last = [5, "Оптимальні стратегії:"]
    index = [res_Wald.index(max(res_Wald))+1,
             res_Max.index(max(res_Max))+1,
             res_Hurwitz.index(max(res_Hurwitz))+1,
             res_Laplace.index(max(res_Laplace))+1,
             res_Bayes_Laplace.index(max(res_Bayes_Laplace))+1]
    data_table.append(last + index)
    
    best = mode(index)
    
    align = []
    for i in range(0, len(head)):
        align.append('c') 
        
    table.add_rows(data_table)
    table.set_cols_align(align)
    table.header(head)
    textbox.insert('insert', table.draw())
    textbox.insert('insert', "\nНайчастіше зустрічайться стратегія №" + str(best))
    
    textbox.configure(state='disabled')

def Clear():
    textbox.delete("1.0","end")

def Wald(matrix):
    minimum = []
    for el in matrix:
        minimum.append(min(el))  
    return minimum

def Max(matrix):
    maximum = []
    for el in matrix:
        maximum.append(max(el))    
    return maximum

def Hurwitz(matrix):
    y = 0.75
    result = []
    for el in matrix:
        result.append(y * min(el) + (1 - y) * max(el))
    return result

def Laplace(matrix):
    result = []
    for el in matrix:
        result.append(np.round(sum(el) / 3, 2))
    return result

def Bayes_Laplace(matrix):
    p = np.array([0.5, 0.35, 0.15])
    result = []
    for el in matrix:
        result.append(sum(el * p))
    return result

matrix = np.loadtxt("1.txt", dtype=int)

main_window = tk.Tk()
main_window.geometry("1200x470")
main_window.resizable(0,0)
main_window.title('Рішення в умовах не визначеності')

str_matrix = ""
for i in range(0, len(matrix)):
    for j in range(0, len(matrix[i])):
        str_matrix += str(matrix[i][j])
        if j != len(matrix)-1:
            str_matrix += "\t"
    if i != j: 
        str_matrix += "\n"

label("Платіжна матриця:").grid(row=0, column=1, columnspan=3, stick='wens', padx=3, pady=3)
label(str_matrix).grid(row=1, column=1, columnspan=3, stick='wens', padx=3, pady=3)

button("Метод Вальда", matrix).grid(row=2, column=1, columnspan=3, stick='wens', padx=3, pady=3)
button("Метод Максимуму", matrix).grid(row=3, column=1, columnspan=3, stick='wens', padx=3, pady=3)
button("Метод Гурвіца", matrix).grid(row=4, column=1, columnspan=3, stick='wens', padx=3, pady=3)
button("Метод Лапласа", matrix).grid(row=5, column=1, columnspan=3, stick='wens', padx=3, pady=3)
button("Метод Байеса-Лапласа", matrix).grid(row=6, column=1, columnspan=3, stick='wens', padx=3, pady=3)

label("Вивід результатів:").grid(row=0, column=4, columnspan=5, stick='wens', padx=3, pady=3)
button_all("Резульати усіх методів", matrix).grid(row=0, column=9, stick='wens', padx=3, pady=3)
textbox = tk.Text(main_window, heigh=20, width=82, state='disabled', font=("Courier", 12, "italic", "bold"))
textbox.grid(row=1, rowspan=6, column=4, columnspan=7, stick='wens', padx=3, pady=3)


for i in range(0, 10):
    main_window.grid_columnconfigure(i, minsize = 50)

for i in range(0, 7):
    main_window.grid_rowconfigure(i, minsize = 50)

main_window.mainloop()