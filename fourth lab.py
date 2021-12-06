import os
from random import randint
import numpy as np
import tkinter as tk
import texttable as tt

def randomize(i, j):
    x = [[randint(1,5) for i in range(i)] for j in range(j)]
    return x

def file(name, i, j):
    file_raiting = []
    if os.stat(name).st_size == 0:
        with open(name, "w+") as file_raiting:
            raiting = randomize(i, j)
            r = np.array(raiting)
            np.savetxt(file_raiting, r, fmt="%4d", delimiter="", newline="\n")
        file_raiting = np.loadtxt(name, dtype=int)
    else:
        file_raiting = np.loadtxt(name, dtype=int)
    return file_raiting

def label(label):
    return tk.Label(text=label, bd=5, font=("Courier", 15, "italic", "bold"), borderwidth=3, relief="solid")
def button_show_expert(text, data):
    return tk.Button(text=text, bd=7, font=("Courier", 15, "italic", "bold"), bg='blue', command=lambda : show_expert(text, data))
def button_show_res(text, data, imp, tv, char):
    return tk.Button(text=text, bd=7, font=("Courier", 13, "italic", "bold"), bg='lime', command=lambda : result(data, imp, tv, char))

def Clear():
    textbox.delete("1.0","end")

def show_expert(expert, mat):
    mat_need = mat[name_file.index(expert)].tolist()
    for i in range(0, len(mat_need)):
        mat_need[i].insert(0, Characteristics[i])
    mat_need.insert(0, [])
    head = TV
    head.insert(0, "")
    
    textbox.configure(state='normal')
    Clear()
    
    table = tt.Texttable()
    align = []
    for i in range(0, len(head)):
        align.append('c')        
    table.add_rows(mat_need)
    table.header(head)
    table.set_cols_align(align)

    textbox.insert('insert', "Оцінки з файлу - " + expert + ":\n")
    textbox.insert('insert', table.draw())
    textbox.configure(state='disabled')
    del head[0]

def result(mat, imp, tv, char):
    add = 0
    for i in range(0, len(mat)):
        add += mat[i]
    imp = np.reshape(imp, (len(imp), 1))
    imp__rait = add * imp
    imp__rait = imp__rait
    
    sum_imp__rait = np.sum(imp__rait, axis=0)
    imp__rait = imp__rait.tolist()
    ctr = 0
    for el in imp__rait:
        el.insert(0, imp[ctr])
        el.insert(0, char[ctr])
        ctr +=1
    sum_imp__rait = sum_imp__rait.tolist()
    sum_imp__rait.insert(0,sum(imp))
    sum_imp__rait.insert(0, "Сума")
    
    imp__rait.append(sum_imp__rait)
    
    head = tv
    head.insert(0, "Ваги")
    head.insert(0, "Параметри")    

    textbox.configure(state='normal')
    Clear()
    
    table = tt.Texttable()
    align = []
    for i in range(0, len(head)):
        align.append('c')     
    imp__rait.insert(0, [])
    table.add_rows(imp__rait)
    table.header(head)
    table.set_cols_align(align)

    textbox.insert('insert', "Вивід таблиці результатів:\n")
    textbox.insert('insert', table.draw())
    textbox.configure(state='disabled')
    del head[0]
    del head[0]
    
Characteristics = []
with open('Characteristics.txt', 'r', encoding="utf-8") as file_char:
    for line in file_char:
        Characteristics.append(line[:-1])

TV = []
with open('TV.txt', 'r', encoding="utf-8") as file_TV:
    for line in file_TV:
        TV.append(line[:-1])
        
importance = []
with open('importance.txt', 'r', encoding="utf-8") as file_imp:
    for line in file_imp:
        importance.append(float(line[:-1]))
main_window = tk.Tk()
main_window.geometry("1050x580")
main_window.resizable(0,0)
main_window.title('Експертна оцінка')

name_file = ["expert_1.txt", "expert_2.txt", "expert_3.txt", "expert_4.txt", "expert_5.txt"]
experts = []
ctr = 0
for el in name_file:
    experts.append(file(el, len(TV), len(Characteristics)))
    button_show_expert(el, experts).grid(row=ctr+1, column=1, columnspan=2, stick='wens', padx=3, pady=3)
    ctr += 1
button_show_res("Таблиця результатів", experts, importance, TV, Characteristics).grid(row=len(name_file)+1, column=1, columnspan=2, stick='wens', padx=3, pady=3)

label("Вивід результатів:").grid(row=0, column=3, columnspan=6, stick='wens', padx=3, pady=3)
textbox = tk.Text(main_window, heigh=32, width=90, state='disabled', font=("Courier", 10, "italic", "bold"))
textbox.grid(row=1, rowspan=len(name_file)+2, column=3, columnspan=6, stick='wens', padx=3, pady=3)

for i in range(0, 10):
    main_window.grid_columnconfigure(i, minsize = 50)

for i in range(0, 7):
    main_window.grid_rowconfigure(i, minsize = 50)

main_window.mainloop()
