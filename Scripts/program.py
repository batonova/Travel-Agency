# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Основной скрипт программы

Авторы: Анисимов А., Батонова О., Батракова Е. (Бригада 4)

"""
import os
import sys
import tkinter as tki
import tkinter.ttk as ttk
import numpy as np
from tkinter.ttk import Combobox 
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from tkinter import messagebox as mb
import pandas as pd
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

workDir = '../'
sys.path.insert(0,workDir+"Library")
import basedf as db

df1 = db.open_table1()
df2 = db.open_table2()
df3 = db.open_table3()

root = tki.Tk()
root.title("База данных - Туристическое агенство")
root.minsize(width=900, height=450)
root.maxsize(width=900, height=1000) 

def show_info(root):
    """
    Входные параметры :  root-главное окно
    Показывает информацию о разработчиках 
    Выходные параметры: None
    Автор: Бригада 4
    """
    window = tki.Toplevel(root)
    window.geometry('400x50')
    window.title("Информация о разработчиках")
    lbl = tki.Label(window, text='Над разработкой этого прекрасного приложения трудились:\n Батонова Оксана,  Анисимов Александр,  Батракова Елена')
    lbl.grid(column=0, row=0)
    
def treeview_sort_column(tv, col, reverse):
    """
    Входные параметры :  tv, col, reverse-переменные для работы с данными
    Производит сортировку столбцов базы данных при нажатии на название кортежа  
    Выходные параметры: None
    Автор: Бригада 4
    """
    
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    if col in ['ID', 'Number', 'Prise', 'Stars']:
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
    else:
        l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: \
           treeview_sort_column(tv, col, not reverse))
    
def show_table_clients(tree1, df1):
    """
    Входные параметры : tree1-переменная для вывода таблицы, df1-таблица «Клиенты» в 3-ей нормальной форме 
    Считывает данные из таблицы «Клиенты» и выводит их в графический интерфейс 
    Выходные параметры: tree1- переменная для вывода таблицы
    Автор: Бригада 4
    """
    tree1["columns"]=("ID", "Surname", "Name", "Otchestvo", "Number")
    tree1.column("#0", width=0, minwidth=0)
    tree1.column("ID", width=20, minwidth=20)
    tree1.column("Surname", width=210, minwidth=210)
    tree1.column("Name", width=210, minwidth=210)
    tree1.column("Otchestvo", width=210, minwidth=210)
    tree1.column("Number", width=250, minwidth=250)             
    tree1.heading("ID", text="ID", command=lambda: \
                     treeview_sort_column(tree1, 'ID', False))
    tree1.heading("Surname", text="Фамилия", command=lambda: \
                     treeview_sort_column(tree1, 'Surname', False))
    tree1.heading("Name", text="Имя", command=lambda: \
                     treeview_sort_column(tree1, 'Name', False))
    tree1.heading("Otchestvo", text="Отчество", command=lambda: \
                     treeview_sort_column(tree1, 'Otchestvo', False))
    tree1.heading("Number", text="Номер", command=lambda: \
                     treeview_sort_column(tree1, 'Number', False))
    count = len(df1)
    for x in range(count):
        tree1.insert("", x, iid=x, values=(df1["ID"][x], df1["Фамилия"][x], 
                                           df1["Имя"][x], df1["Отчество"][x], 
                                           df1["Номер телефона"][x]))
    tree1.selectmode = "extended"
    tree1.bind("<<TreeviewSelect>>", "+")
    tree1.pack(expand=1, fill='both')
    return tree1

def show_table_trips(tree2, df2):
    """
    Входные параметры : tree2-переменная для вывода таблицы, df2-таблица «Поездки» в 3-ей нормальной форме
    Считывает данные из таблицы «Поездки» и выводит их в графический интерфейс 
    Выходные параметры: tree2- переменная для вывода таблицы
    Автор: Бригада 4
    """
    tree2["columns"]=("ID", "Date", "Hotel", "Status", "Prise")
    tree2.column("#0", width=0, minwidth=0)
    tree2.column("ID", width=20, minwidth=20)
    tree2.column("Date", width=210, minwidth=210)
    tree2.column("Hotel", width=210, minwidth=210)
    tree2.column("Status", width=210, minwidth=210)
    tree2.column("Prise", width=250, minwidth=250)             
    tree2.heading("ID", text="ID", command=lambda: \
                     treeview_sort_column(tree2, 'ID', False))
    tree2.heading("Date", text="Дата вылета", command=lambda: \
                     treeview_sort_column(tree2, 'Date', False))
    tree2.heading("Hotel", text="Название отеля", command=lambda: \
                     treeview_sort_column(tree2, 'Hotel', False))
    tree2.heading("Status", text="Статус оплаты", command=lambda: \
                     treeview_sort_column(tree2, 'Status', False))
    tree2.heading("Prise", text="Стоимость", command=lambda: \
                     treeview_sort_column(tree2, 'Prise', False))
    count = len(df2)
    global from_price, to_price, status
    if status == 0: return
    for x in range(count):
        if df2["Стоимость"][x] >= from_price and df2["Стоимость"][x] <= to_price \
           and ((status == 1 and df2["Статус оплаты"][x] == "забронировано") or \
           (status == 2 and df2["Статус оплаты"][x] == "оплачено") or status == 3):
            tree2.insert("", x, iid=x, values=(df2["ID"][x], df2["Дата вылета"][x], 
                                               df2["Название отеля"][x], 
                                               df2["Статус оплаты"][x], 
                                               df2["Стоимость"][x]))
    tree2.selectmode = "extended"
    tree2.bind("<<TreeviewSelect>>", "+")
    tree2.pack(expand=1, fill='both')
    return tree2

def show_table_hotels(tree3, df3):
    """
    Входные параметры : tree3-переменная для вывода таблицы, df3-таблица «Отели» в 3-ей нормальной форме
    Считывает данные из таблицы «Отели» и выводит их в графический интерфейс 
    Выходные параметры: tree3- переменная для вывода таблицы
    Автор: Бригада 4
    """
    tree3["columns"]=("Hotel", "Country", "City", "Stars")
    tree3.column("#0", width=0, minwidth=0)
    for x in tree3["columns"]:
        tree3.column(x, width=225,minwidth=225)             
    tree3.heading("Hotel", text="Название отеля", command=lambda: \
                     treeview_sort_column(tree3, 'Hotel', False))
    tree3.heading("Country", text="Страна прибытия", command=lambda: \
                     treeview_sort_column(tree3, 'Country', False))
    tree3.heading("City", text="Город прибытия", command=lambda: \
                     treeview_sort_column(tree3, 'City', False))
    tree3.heading("Stars", text="Количество звёзд", command=lambda: \
                     treeview_sort_column(tree3, 'Stars', False))
    count = len(df3)
    global from_stars, to_stars
    for x in range(count):
        if (df3["Количество звёзд"][x] >= from_stars and df3["Количество звёзд"][x] <= to_stars):
            tree3.insert("", x, iid=x, values=(df3["Название отеля"][x], 
                                               df3["Страна прибытия"][x], 
                                               df3["Город прибытия"][x], 
                                               df3["Количество звёзд"][x]))
    tree3.selectmode = "extended"
    tree3.bind("<<TreeviewSelect>>", "+")
    tree3.pack(expand=1, fill='both')
    return tree3

def show_table_all(tree4, df4):
    """
    Входные параметры : tree4-переменная для вывода таблицы, df4-таблица «Общая» в 3-ей нормальной форме
    Считывает данные из таблицы «Общая» и выводит их в графический интерфейс 
    Выходные параметры: tree4- переменная для вывода таблицы
    Автор: Бригада 4
    """
    tree4["columns"]=("ID", "Surname", "Name", "Otchestvo", "Number", 
                      "Date", "Hotel", "Status", "Prise", "Country", 
                      "City", "Stars")
    tree4.column("#0", width=0, minwidth=0)
    for x in tree4["columns"]:
        tree4.column(x, width=75,minwidth=75)
    tree4.heading("ID", text="ID", command=lambda: \
                     treeview_sort_column(tree4, 'ID', False))
    tree4.heading("Surname", text="Фамилия", command=lambda: \
                     treeview_sort_column(tree4, 'Surname', False))
    tree4.heading("Name", text="Имя", command=lambda: \
                     treeview_sort_column(tree4, 'Name', False))
    tree4.heading("Otchestvo", text="Отчество", command=lambda: \
                     treeview_sort_column(tree4, 'Otchestvo', False))
    tree4.heading("Number", text="Номер", command=lambda: \
                     treeview_sort_column(tree4, 'Number', False))
    tree4.heading("Date", text="Дата вылета", command=lambda: \
                     treeview_sort_column(tree4, 'Date', False))
    tree4.heading("Hotel", text="Название отеля", command=lambda: \
                     treeview_sort_column(tree4, 'Hotel', False))
    tree4.heading("Status", text="Статус оплаты", command=lambda: \
                     treeview_sort_column(tree4, 'Status', False))
    tree4.heading("Prise", text="Стоимость", command=lambda: \
                     treeview_sort_column(tree4, 'Prise', False))
    tree4.heading("Country", text="Страна прибытия", command=lambda: \
                     treeview_sort_column(tree4, 'Country', False))
    tree4.heading("City", text="Город прибытия", command=lambda: \
                     treeview_sort_column(tree4, 'City', False))
    tree4.heading("Stars", text="Количество звёзд", command=lambda: \
                     treeview_sort_column(tree4, 'Stars', False))
    count = len(df4)
    global from_stars, to_stars, from_price, to_price, status
    if status == 0: return
    for x in range(count):
        if (df4["Стоимость"][x] >= from_price and df4["Стоимость"][x] <= to_price) \
        and (df4["Количество звёзд"][x] >= from_stars and df4["Количество звёзд"][x] <= to_stars) \
        and ((status == 1 and df4["Статус оплаты"][x] == "забронировано") \
        or (status == 2 and df4["Статус оплаты"][x] == "оплачено") or status == 3):
            tree4.insert("", x, iid=x, values=(df4["ID"][x], df4["Фамилия"][x], 
                                               df4["Имя"][x], df4["Отчество"][x], 
                                               df4["Номер телефона"][x], 
                                               df4["Дата вылета"][x], 
                                               df4["Название отеля"][x], 
                                               df4["Статус оплаты"][x], 
                                               df4["Стоимость"][x], 
                                               df4["Страна прибытия"][x], 
                                               df4["Город прибытия"][x], 
                                               df4["Количество звёзд"][x]))
    tree4.selectmode = "none"
    tree4.bind("<<TreeviewSelect>>", "+")
    tree4.pack(expand=1, fill='both')
    return tree4

def delete(tree1, tree2, tree3, tree4):
    
    """
    Входные параметры : tree1, tree2, tree3, tree4-переменный для работы с данными
    Удаляет выделенную строку из базы данных 
    Выходные параметры: None
    Автор: Бригада 4
    """
    
    global df1, df2, df3, df4
    if tab_control.index(tab_control.select()) == 0:
        m = tree1.selection()
        if len(m) != 0:
            answer = mb.askyesno(title="Удаление", message="При удалении данных о клиенте, будут удалены все его поездки. Продолжить?")
            if answer == True:
                for x in m:
                    for y in df2.index:
                        if df1["ID"][int(x)] == df2["ID"][y]:
                            df2 = df2.drop(y)
                df2.index = range(len(df2))
                            
                df1 = (df1.drop(list(map(int, tree1.selection())))).reset_index(drop=True)
                for i in tree1.get_children():
                    tree1.delete(i)
                tree1 = show_table_clients(tree1, df1)
                for i in tree2.get_children():
                    tree2.delete(i)
                tree2 = show_table_trips(tree2, df2)
                df4 = db.make_table4(df1, df2, df3)
                for i in tree4.get_children():
                    tree4.delete(i)
                tree4 = show_table_all(tree4, df4)
        else:
            mb.showerror("Ошибка", "Не выбран ни один клиент для удаления")
    if tab_control.index(tab_control.select()) == 1:
        m = tree2.selection()
        if len(m) != 0:
            df2 = (df2.drop(list(map(int, tree2.selection())))).reset_index(drop=True)
            for i in tree2.get_children():
                tree2.delete(i)
            tree2 = show_table_trips(tree2, df2)
            df4 = db.make_table4(df1, df2, df3)
            for i in tree4.get_children():
                tree4.delete(i)
            tree4 = show_table_all(tree4, df4)
        else:
            mb.showerror("Ошибка", "Не выбрана ни одна поездка для удаления")
    if tab_control.index(tab_control.select()) == 2:
        m = tree3.selection()
        if len(m) != 0:
            answer = mb.askyesno(title="Удаление", message="При удалении данных об отеле, будут удалены все поездки в этот отель. Продолжить?")
            if answer == True:
                for x in m:
                    for y in df2.index:
                        if df3["Название отеля"][int(x)] == df2["Название отеля"][y]:
                            df2 = df2.drop(y)
                df2.index = range(len(df2))
                            
                df3 = (df3.drop(list(map(int, tree3.selection())))).reset_index(drop=True)
                for i in tree3.get_children():
                    tree3.delete(i)
                tree1 = show_table_hotels(tree3, df3)
                for i in tree2.get_children():
                    tree2.delete(i)
                tree2 = show_table_trips(tree2, df2)
                df4 = db.make_table4(df1, df2, df3)
                for i in tree4.get_children():
                    tree4.delete(i)
                tree4 = show_table_all(tree4, df4)
        else:
            mb.showerror("Ошибка", "Не выбран ни один отель для удаления")

def add_client(tree1, tree4):
    """
    Входные параметры : tree1, tree4-переменный для работы с данными
    Добавляет данные о новом клиенте 
    Выходные параметры: None
    Автор: Бригада 4
    """
    global df1, df4, df2, df3
    window = tki.Tk()
    window.title("Добавление нового клиента")
    window.minsize(600,100)
    
    def clickMe():
        global tree1, df1, tree4, df4, df2, df3
        if len(id_.get())!=0 and (int(id_.get()) not in list(df1["ID"])) and \
            len(fam.get())!=0 and len(name.get())!=0 and len(ot.get())!=0 and \
            len(num.get())!=0:
            df1.loc[len(df1.index)]= [int(id_.get()),fam.get(),name.get(),ot.get(),int(num.get())]
            
            for i in tree1.get_children():
                tree1.delete(i)
            tree1 = show_table_clients(tree1, df1)
        else:
            if int(id_.get()) in list(df1["ID"]):
                mb.showerror("Ошибка", "Клиент с таким ID уже существует")
            else:
                mb.showerror("Ошибка", "Остались незаполненные поля")
        window.destroy()
        
    label = tki.Label(window, text = "Введите id")
    label.grid(column = 0, row = 0)
    label = tki.Label(window, text = "Введите фамилию")
    label.grid(column = 1, row = 0)
    label = tki.Label(window, text = "Введите имя")
    label.grid(column = 2, row = 0)
    label = tki.Label(window, text = "Введите отчество")
    label.grid(column = 3, row = 0)
    label = tki.Label(window, text = "Введите номер телефона")
    label.grid(column = 4, row = 0)

    id_= tki.Entry(window)
    id_.grid(row=1,column=0, padx=5, pady=5) 
    
    fam= tki.Entry(window)
    fam.grid(row=1,column=1, padx=5, pady=5) 
    
    name= tki.Entry(window)
    name.grid(row=1,column=2, padx=5, pady=5) 
    
    ot= tki.Entry(window)
    ot.grid(row=1,column=3, padx=5, pady=5) 
    
    num= tki.Entry(window)
    num.grid(row=1,column=4, padx=5, pady=5) 
 
    button = ttk.Button(window, text = "Добавить", command = clickMe)
    button.grid(column= 3, row = 2)
    
    window.mainloop()

def add_trip(tree2, tree4):
    """
    Входные параметры : tree2, tree4-переменный для работы с данными
    Добавляет новую поездку
    Выходные параметры: None
    Автор: Бригада 4
    """
    global df2, df1, df3, df4
    window = tki.Tk()
    window.title("Добавление новой поездки")
    window.minsize(600,110)
    
    def clickMe():
        global tree2, df2, df1, df3, tree4, df4
        flag = False
        indx = list(df2.loc[df2["Дата вылета"] == d.get()].index)
        for x in indx:
            if df2["ID"][x] == int(id_.get()):
                flag = True
        if (len(id_.get())!=0 and len(d.get())!=0 and len(n.get())!=0 and \
            len(combo.get())!=0 and not flag):
            df2.loc[len(df2.index)]= [int(id_.get()),d.get(),n.get(),combo.get(),int(p.get())]
            for i in tree2.get_children():
                tree2.delete(i)
            tree2 = show_table_trips(tree2, df2)
            df4 = db.make_table4(df1, df2, df3)
            for i in tree4.get_children():
                tree4.delete(i)
            tree4 = show_table_all(tree4, df4)
        else:
            if flag:
                mb.showerror("Ошибка", "У данного клиента уже существует поездка в этот день")
            else:
                mb.showerror("Ошибка", "Остались незаполненные поля")
        window.destroy()
    
    label = tki.Label(window, text = "Введите id")
    label.grid(column = 0, row = 0)
    label = tki.Label(window, text = "Введите дату вылета")
    label.grid(column = 1, row = 0)
    label = tki.Label(window, text = "Введите название отеля")
    label.grid(column = 2, row = 0)
    label = tki.Label(window, text = "Введите статус оплаты")
    label.grid(column = 3, row = 0)
    label = tki.Label(window, text = "Введите стоимость")
    label.grid(column = 4, row = 0)

    id_ = Combobox(window, state='readonly')  
    id_['values'] = [x for x in df1["ID"]]
    id_.grid(row=1,column=0, padx=5, pady=5)
    
    d = tki.Entry(window)
    d.grid(row=1,column=1, padx=5, pady=5)
         
    n = Combobox(window, state='readonly')  
    n['values'] = [x for x in df3["Название отеля"]]
    n.grid(row=1,column=2, padx=5, pady=5)     
    
    combo = Combobox(window, state='readonly')  
    combo['values'] = ("оплачено", "забронировано")  
    combo.current(1) 
    combo.grid(column=3, row=1, padx=5, pady=5) 
    
    p= tki.Scale(window, orient="horizontal", length=190, from_=0, to=1500000, 
                 tickinterval=500000, resolution=10000)
    p.grid(row=1,column=4, padx=5, pady=5) 
 
    button = ttk.Button(window, text = "Добавить", command = clickMe)
    button.grid(column= 3, row = 2)
    
    window.mainloop()

def add_hotel(tree3, tree4):
    """
    Входные параметры : tree3, tree4-переменный для работы с данными
    Добавляет данные о новом отеле 
    Выходные параметры: None
    Автор: Бригада 4
    """
    global df3, df4, df1, df2
    window = tki.Tk()
    window.title("Добавление нового отеля")
    window.minsize(600,100)
    
    def clickMe():
        global tree3, df3, tree4, df4, df1, df2
        if len(hotel.get())!=0 and (hotel.get() not in list(df3["Название отеля"])) \
            and len(country.get())!=0 and len(city.get())!=0 and len(combo.get())!=0:
            df3.loc[len(df3.index)]= [hotel.get(),country.get(),city.get(),int(combo.get())]
            for i in tree3.get_children():
                tree3.delete(i)
            tree3 = show_table_hotels(tree3, df3)
        else:
            if hotel.get() in list(df3["Название отеля"]):
                mb.showerror("Ошибка", "Отель с таким названием уже существует")
            else:
                mb.showerror("Ошибка", "Остались незаполненные поля")
        window.destroy()
    
    label = tki.Label(window, text = "Введите название отеля")
    label.grid(column = 0, row = 0)
    label = tki.Label(window, text = "Введите страну")
    label.grid(column = 1, row = 0)
    label = tki.Label(window, text = "Введите город")
    label.grid(column = 2, row = 0)
    label = tki.Label(window, text = "Введите количество звезд")
    label.grid(column = 3, row = 0)

    hotel = tki.Entry(window)
    hotel.grid(row=1,column=0, padx=5, pady=5) 
    
    country = tki.Entry(window)
    country.grid(row=1,column=1, padx=5, pady=5) 
    
    city = tki.Entry(window)
    city.grid(row=1,column=2, padx=5, pady=5) 
     
    combo = Combobox(window, state='readonly')  
    combo['values'] = ("1", "2","3","4", "5")  
    combo.current(0)  
    combo.grid(column=3, row=1, padx=5, pady=5) 
 
    button = ttk.Button(window, text = "Добавить", command = clickMe)
    button.grid(column= 3, row = 2)
    
    window.mainloop()

def find():
    """
    Входные параметры : None
    Выполняет поиск заданного элемента. Поиск происходит по общей таблице  
    Выходные параметры: None
    Автор: Бригада 4
    """
    global df4
    window = tki.Tk()
    window.title("Поиск")
    window.minsize(250,250)
    
    def clickMe():
        lbl1 = tki.Label(window, text="ID")
        lbl1.grid(column=0, row=8)
        lbl2 = tki.Label(window, text="Фамилия")
        lbl2.grid(column=1, row=8)
        lbl3 = tki.Label(window, text="Имя")
        lbl3.grid(column=2, row=8)
        lbl4 = tki.Label(window, text="Отчество")
        lbl4.grid(column=3, row=8)
        lbl5 = tki.Label(window, text="Номер телефона")
        lbl5.grid(column=4, row=8)
        lbl6 = tki.Label(window, text="Дата вылета")
        lbl6.grid(column=5, row=8)
        lbl7 = tki.Label(window, text="Название отеля")
        lbl7.grid(column=6, row=8)
        lbl8 = tki.Label(window, text="Статус оплаты")
        lbl8.grid(column=7, row=8)
        lbl9 = tki.Label(window, text="Стоимость")
        lbl9.grid(column=8, row=8)
        lbl10 = tki.Label(window, text="Страна прибытия")
        lbl10.grid(column=9, row=8)
        lbl11 = tki.Label(window, text="Город прибытия")
        lbl11.grid(column=10, row=8)
        lbl12 = tki.Label(window, text="Количество звёзд")
        lbl12.grid(column=11, row=8)
        e=8
        for i in range(0,len(df4.index),1):
            if str(z.get())==str(df4.loc[i,combo.get()]):
                e=e+1
                lbl1 = tki.Label(window, text=df4.loc[i,'ID'])
                lbl1.grid(column=0, row=e)
                lbl2 = tki.Label(window, text=df4.loc[i,'Фамилия'])
                lbl2.grid(column=1, row=e)
                lbl3 = tki.Label(window, text=df4.loc[i,'Имя'])
                lbl3.grid(column=2, row=e)
                lbl4 = tki.Label(window, text=df4.loc[i,'Отчество'])
                lbl4.grid(column=3, row=e)
                lbl5 = tki.Label(window, text=df4.loc[i,'Номер телефона'])
                lbl5.grid(column=4, row=e)
                lbl6 = tki.Label(window, text=df4.loc[i,'Дата вылета'])
                lbl6.grid(column=5, row=e)
                lbl7 = tki.Label(window, text=df4.loc[i,'Название отеля'])
                lbl7.grid(column=6, row=e)
                lbl8 = tki.Label(window, text=df4.loc[i,'Статус оплаты'])
                lbl8.grid(column=7, row=e)
                lbl9 = tki.Label(window, text=df4.loc[i,'Стоимость'])
                lbl9.grid(column=8, row=e)
                lbl10 = tki.Label(window, text=df4.loc[i,'Страна прибытия'])
                lbl10.grid(column=9, row=e)
                lbl11 = tki.Label(window, text=df4.loc[i,'Город прибытия'])
                lbl11.grid(column=10, row=e)
                lbl12 = tki.Label(window, text=df4.loc[i,'Количество звёзд'])
                lbl12.grid(column=11, row=e)
           
    label = tki.Label(window, text = "Выберите атрибут, который вы хотите найти:")
    label.grid(column = 6, row = 0)
    label = tki.Label(window, text = "Введите его значение:")
    label.grid(column = 6, row = 2) 
    
    combo = Combobox(window)  
    combo['values'] = ("ID", "Фамилия","Имя","Отчество", "Номер телефона",
                       "Дата вылета","Название отеля","Статус оплаты",
                       "Стоимость","Страна прибытия","Город прибытия",
                       "Количество звёзд")  
    combo.current(0)  
    combo.grid(column=6, row=1) 
    
    
    z= tki.Entry(window)
    z.grid(row=3,column=6, padx=5, pady=5) 
    
    button = ttk.Button(window, text = "Найти", command = clickMe)
    button.grid(column= 6, row = 6)
    
    
    window.mainloop()
    
def change(tree1, tree2, tree3, tree4):
    
    """
    Входные параметры : tree1, tree2, tree3, tree4-переменный для работы с данными
    Редактирует выделенную строку из базы данных (редактировать можно только 
    первые 3 таблицы в 3НФ)
    Выходные параметры: None
    Автор: Бригада 4
    """
    
    global df1, df2, df3, df4
    if tab_control.index(tab_control.select()) == 0:
        m = tree1.selection()
        if len(m) != 0:
            window = tki.Tk()
            window.title("Редактировать данные о клиенте")
            window.minsize(300,105)
            
            def clickMe():
                global tree4, df1, tree1
                df1.loc[int(m[0]), "Фамилия"] = fam.get()
                df1.loc[int(m[0]), "Имя"] = name.get()
                df1.loc[int(m[0]), "Отчество"] = ot.get()
                df1.loc[int(m[0]), "Номер телефона"] = int(num.get())
                window.destroy()
                for i in tree1.get_children():
                    tree1.delete(i)
                tree1 = show_table_clients(tree1, df1)
                df4 = db.make_table4(df1, df2, df3)
                for i in tree4.get_children():
                    tree4.delete(i)
                tree4 = show_table_all(tree4, df4)
                
            label = tki.Label(window, text = "ID клиента")
            label.grid(column = 0, row = 0)
            label = tki.Label(window, text = "Введите фамилию")
            label.grid(column = 1, row = 0)
            label = tki.Label(window, text = "Введите имя")
            label.grid(column = 2, row = 0)
            label = tki.Label(window, text = "Введите отчество")
            label.grid(column = 3, row = 0)
            label = tki.Label(window, text = "Введите номер телефона")
            label.grid(column = 4, row = 0)
            
            lbl = tki.Label(window, text=df1["ID"][int(m[0])])
            lbl.grid(row=1,column=0, padx=5, pady=5) 
            
            fam = tki.Entry(window)
            famn = str(df1["Фамилия"][int(m[0])])
            fam.insert("end", famn)
            fam.grid(row=1,column=1, padx=5, pady=5) 
            
            name= tki.Entry(window)
            namen = df1["Имя"][int(m[0])]
            name.insert("end", namen)
            name.grid(row=1,column=2, padx=5, pady=5) 
            
            ot= tki.Entry(window)
            otn = str(df1["Отчество"][int(m[0])])
            ot.insert("end", otn)
            ot.grid(row=1,column=3, padx=5, pady=5) 
            
            num= tki.Entry(window)
            numn = str(df1["Номер телефона"][int(m[0])])
            num.insert("end", numn)
            num.grid(row=1,column=4, padx=5, pady=5)
            
            button = ttk.Button(window, text = "Изменить", command = clickMe)
            button.grid(column= 0, row = 7)
            
            window.mainloop()
        else:
            mb.showerror("Ошибка", "Не выбран клиент для редактирования")
    if tab_control.index(tab_control.select()) == 1:
        m = tree2.selection()
        if len(m) != 0:
            window = tki.Tk()
            window.title("Редактировать данные о поездках")
            window.minsize(300,100)
            
            def clickMe():
                global tree4, df1, tree2
                df2.loc[int(m[0]), "ID"] = int(id_.get())
                df2.loc[int(m[0]), "Дата вылета"] = data.get()
                df2.loc[int(m[0]), "Название отеля"] = hotel.get()
                df2.loc[int(m[0]), "Статус оплаты"] = status.get()
                df2.loc[int(m[0]), "Стоимость"] = int(price.get())
                window.destroy()
                for i in tree2.get_children():
                    tree2.delete(i)
                tree2 = show_table_trips(tree2, df2)
                df4 = db.make_table4(df1, df2, df3)
                for i in tree4.get_children():
                    tree4.delete(i)
                tree4 = show_table_all(tree4, df4)
                
            label = tki.Label(window, text = "Введите id")
            label.grid(column = 0, row = 0)
            label = tki.Label(window, text = "Введите дату вылета")
            label.grid(column = 1, row = 0)
            label = tki.Label(window, text = "Введите название отеля")
            label.grid(column = 2, row = 0)
            label = tki.Label(window, text = "Введите статус оплаты")
            label.grid(column = 3, row = 0)
            label = tki.Label(window, text = "Введите стоимость")
            label.grid(column = 4, row = 0)
            
            id_ = Combobox(window, state='readonly')  
            id_['values'] = [x for x in df1["ID"]]
            idn = int(df2["ID"][int(m[0])])
            id_.current(idn-1)
            id_.grid(row=1,column=0, padx=5, pady=5)
            
            data = tki.Entry(window)
            datan = df2["Дата вылета"][int(m[0])]
            data.insert('end', datan)
            data.grid(row=1,column=1, padx=5, pady=5) 
             
            hotel = Combobox(window, state='readonly')  
            hotel['values'] = [x for x in df3["Название отеля"]]
            t = 0
            hoteln = df2["Название отеля"][int(m[0])]
            for x in hotel['values']:
                if hoteln == x: break
                t = t + 1
            hotel.current(t)
            hotel.grid(row=1,column=2, padx=5, pady=5)
            
            status = Combobox(window, state='readonly')  
            status['values'] = ("оплачено", "забронировано") 
            if df2["Статус оплаты"][int(m[0])] == "забронировано":
                status.current(1) 
            else:
                status.current(0)
            status.grid(row=1,column=3, padx=5, pady=5) 
            
            price = tki.Scale(window, orient="horizontal", length=190, from_=0, to=1500000, 
                             tickinterval=500000, resolution=10000)
            pricen = str(df2["Стоимость"][int(m[0])])
            price.set(pricen)
            price.grid(row=1,column=4, padx=5, pady=5)
            
            button = ttk.Button(window, text = "Изменить", command = clickMe)
            button.grid(column= 0, row = 7)
            
            window.mainloop()
        else:
            mb.showerror("Ошибка", "Не выбрана поездка для редактирования")
    if tab_control.index(tab_control.select()) == 2:
        m = tree3.selection()
        if len(m) != 0:
            window = tki.Tk()
            window.title("Редактировать данные об отелях")
            window.minsize(300,100)
            
            def clickMe():
                global tree4, df1, tree2, tree3
                df3.loc[int(m[0]), "Страна прибытия"] = country.get()
                df3.loc[int(m[0]), "Город прибытия"] = city.get()
                df3.loc[int(m[0]), "Количество звёзд"] = int(stars.get())
                window.destroy()
                for i in tree3.get_children():
                    tree3.delete(i)
                tree3 = show_table_hotels(tree3, df3)
                df4 = db.make_table4(df1, df2, df3)
                for i in tree4.get_children():
                    tree4.delete(i)
                tree4 = show_table_all(tree4, df4)
                
            label = tki.Label(window, text = "Название отеля")
            label.grid(column = 0, row = 0)
            label = tki.Label(window, text = "Введите страну")
            label.grid(column = 1, row = 0)
            label = tki.Label(window, text = "Введите город")
            label.grid(column = 2, row = 0)
            label = tki.Label(window, text = "Введите количество звёзд")
            label.grid(column = 3, row = 0)
            
            lbl = tki.Label(window, text=df3["Название отеля"][int(m[0])])
            lbl.grid(row=1,column=0, padx=5, pady=5) 
            
            country = tki.Entry(window)
            countryn = df3["Страна прибытия"][int(m[0])]
            country.insert("end", countryn)
            country.grid(row=1,column=1, padx=5, pady=5) 
            
            city = tki.Entry(window)
            cityn = df3["Город прибытия"][int(m[0])]
            city.insert("end", cityn)
            city.grid(row=1,column=2, padx=5, pady=5) 
            
            stars = Combobox(window, state='readonly')  
            stars['values'] = ("1", "2", "3", "4", "5")
            starsn = df3["Количество звёзд"][int(m[0])]
            stars.current(starsn-1)
            stars.grid(row=1,column=3, padx=5, pady=5) 
            
            button = ttk.Button(window, text = "Изменить", command = clickMe)
            button.grid(column= 0, row = 7)
            
            window.mainloop()
        else:
            mb.showerror("Ошибка", "Не выбран отель для редактирования")
    
def Graf1(df1):
    """
    Входные параметры : df1-(DataFrame) данные по таблице «Клиенты»
    Выполняет построение кластеризованной столбчатой диаграммы, которая 
    показывае пару качественных атрибутов "Имя" и "Фамилия"
    Выходные параметры: None
    Автор: Бригада 4
    """
    window = tki.Toplevel(root)
    window.minsize(width=800, height=550)
    window.wm_title("Кластеризованная столбчатая диаграмма (атрибуты \"Имя\" и \"Фамилия\"")
    fig = Figure(figsize=(8,6))
    fig.add_subplot(111).bar(df1['Имя'], df1['Фамилия'],linewidth=2)
    
    canvas = FigureCanvasTkAgg(fig, master=window)  
    canvas.draw()
    canvas.get_tk_widget().place(x=25, y=10)
    
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)
    
    tki.mainloop()
    
def Graf2(df3):
    """
    Входные параметры : df3-(DataFrame) данные по таблице «Отели»
    Выполняет построение категоризированной гистограммы по количеству 
    отелей с разным числом звёзд  
    Выходные параметры: None
    Автор: Бригада 4
    """
    window = tki.Toplevel(root)
    window.minsize(width=800, height=550)
    window.wm_title("Категоризированная гистограмма по количеству отелей с разным числом звёзд")
    fig = Figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    ax.set_title('Количество звёзд у отеля')
    ax.set_xlabel('Звёзды')
    ax.set_ylabel('Количество отелей"')
    ax.hist(df3['Количество звёзд'][:8],normed=0)
    canvas = FigureCanvasTkAgg(fig, master=window)  
    canvas.draw()
    canvas.get_tk_widget().place(x=25, y=10)
    
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)
    
    tki.mainloop()
    
def Graf3(df4):
    """
    Входные параметры : df4-(DataFrame) данные по таблице «Общая таблица»
    Выполняет построение категоризированной диаграммы Бокса-Вискера по 
    стоимости поездок  
    Выходные параметры: None
    Автор: Бригада 4
    """
    window = tki.Toplevel(root)
    window.minsize(width=800, height=550)
    window.wm_title("Категоризированная диаграмма Бокса-Вискера по стоимости поездок")
    ax = plt.subplots()
    fig = Figure(figsize=(8,6))
    
    ax = fig.add_subplot(111)
    ax.set_title('Стоимость')
    
    ax.boxplot(df4['Стоимость'], showfliers=False)
    canvas = FigureCanvasTkAgg(fig, master=window)  
    canvas.draw()
    canvas.get_tk_widget().place(x=25, y=10)
    
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)
    
    tki.mainloop()
    
def Graf4(df4):
    """
    Входные параметры : df4-(DataFrame) данные по таблице «Общая таблица»
    Выполняет построение категоризированной диаграммы рассеивания 
    по стоимости для отелей с разным количеством звёзд
    Выходные параметры: None
    Автор: Бригада 4
    """
    window = tki.Toplevel(root)
    window.minsize(width=800, height=550)
    window.wm_title("Категоризированной диаграмма рассеивания по стоимости для отелей с разным количеством звёзд")
    fig = Figure(figsize=(8,6))
    col = df4[["Количество звёзд","Стоимость"]].dropna(how="any")
    vals = col.values
    ax = fig.add_subplot(111)
    ax.set_xlabel('Количество звёзд')
    ax.set_ylabel('Стоимость')
    ax.scatter(vals[:, 0], vals[:, 1])
    canvas = FigureCanvasTkAgg(fig, master=window)  
    canvas.draw()
    canvas.get_tk_widget().place(x=25, y=10)
    
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tki.TOP, fill=tki.BOTH, expand=1)
    
    tki.mainloop()
    
def filter_func(tree2, tree3, tree4, cmb1, cmb2, sc1, sc2, br, op):
    """
    Входные параметры : tree1, tree2, tree3, tree4-переменный для работы с данными
                        cmb1, cmb2, sc1, sc2, br, op - переменные для выбранных 
                        пользователем ограничений
    Фильтрует строки по выбранным параметрам и выводит их 
    Выходные параметры: None
    Автор: Бригада 4
    """
    global from_stars, to_stars, from_price, to_price, status
    from_stars = int(cmb1)
    to_stars = int(cmb2)
    from_price = sc1
    to_price = sc2
    if br == 1 and op == 1:
        status = 3
    else:
        if br != 1 and op == 1:
            status = 2
        else:
            if op != 1 and br:
                status = 1
            else:
                status = 0
    for i in tree2.get_children():
            tree2.delete(i)
    tree2 = show_table_trips(tree2, df2)
    for i in tree3.get_children():
            tree3.delete(i)
    tree3 = show_table_hotels(tree3, df3)
    df4 = db.make_table4(df1, df2, df3)
    for i in tree4.get_children():
            tree4.delete(i)
    tree4 = show_table_all(tree4, df4) 
    
def new_bases():
    """
    Входные параметры : None
    Создает пустые нормализованные базы данных
    Выходные параметры: None
    Автор: Бригада 4
    """
    global df1, df2, df3, tree1, tree2, tree3, tree4
    clients = pd.DataFrame({"ID": [], "Фамилия": [], "Имя": [], "Отчество": [], "Номер телефона": []})
    trips = pd.DataFrame({"ID": [], "Дата вылета": [], "Название отеля": [], 
                        "Статус оплаты": [], "Стоимость": []})
    hotels = pd.DataFrame({"Название отеля": [], "Страна прибытия": [], 
                        "Город прибытия": [], "Количество звёзд": []})
    df1 = clients
    df2 = trips
    df3 = hotels
    for i in tree1.get_children():
        tree1.delete(i)
    tree1 = show_table_clients(tree1, df1)
    for i in tree2.get_children():
        tree2.delete(i)
    tree2 = show_table_trips(tree2, df2)
    for i in tree3.get_children():
        tree3.delete(i)
    tree3 = show_table_hotels(tree3, df3)
    df4 = db.make_table4(df1, df2, df3)
    for i in tree4.get_children():
        tree4.delete(i)
    tree4 = show_table_all(tree4, df4)   
    
def basestat(df4):
    """
    Входные параметры : df4 - объединенная база данных
    Формирует и сохраняет таблицу с базовой статистикой по выбранным атрибутам
    Выходные параметры: None
    Автор: Бригада 4
    """
    window = tki.Toplevel(root)
    window.geometry('200x520')
    window.title("Базовая статистика") 
    lbl = tki.Label(window, text="Выберите атрибуты\nдля формирования отчёта:", padx="15", pady="6")
    lbl.pack()
    
    def clck():
        statb = pd.DataFrame()
        if c1.get() == 1:
            statb["ID"] = df4["ID"]
        if c2.get() == 1:
            statb["Фамилия"] = df4["Фамилия"]
        if c3.get() == 1:
            statb["Имя"] = df4["Имя"]
        if c4.get() == 1:
            statb["Отчество"] = df4["Отчество"]
        if c5.get() == 1:
            statb["Номер телефона"] = df4["Номер телефона"]
        if c6.get() == 1:
            statb["Дата вылета"] = df4["Дата вылета"]
        if c7.get() == 1:
            statb["Название отеля"] = df4["Название отеля"]
        if c8.get() == 1:
            statb["Статус оплаты"] = df4["Статус оплаты"]
        if c9.get() == 1:
            statb["Стоимость"] = df4["Стоимость"]
        if c10.get() == 1:
            statb["Страна прибытия"] = df4["Страна прибытия"]
        if c11.get() == 1:
            statb["Город прибытия"] = df4["Город прибытия"]
        if c12.get() == 1:
            statb["Количество звёзд"] = df4["Количество звёзд"]

        window.destroy()
        if (c1.get() == 1 or c2.get() == 1 or c3.get() == 1 or c4.get() == 1 
            or c5.get() == 1 or c6.get() == 1 or c7.get() == 1 or c8.get() == 1
            or c9.get() == 1 or c10.get() == 1 or c11.get() == 1 or c12.get() == 1):
            analys = statb.describe(include='all')
            window2 = tki.Toplevel(root)
            window2.geometry('800x350')
            window2.title("Базовая статистика") 
            tree = ttk.Treeview(window2)
            tree["columns"] = ["Свойства"]+list(analys)
            tree.column("#0", width=0, minwidth=0)
            for x in tree["columns"]:
                tree.column(x, width=75,minwidth=75)
            for x in tree["columns"]:
                tree.heading(x, text=x)
            if "first" in list(analys):
                analys.drop(["first"], inplace=True)
            if "last" in list(analys):
                analys.drop(["last"], inplace=True)
            name = ["Общее количество:", "Уникальные элементы:", 
                    "Самый частоповторяющийся элемент:", "Количество повторений:",
                    "Среднее значение:", "Среднеквадратичное:", "Минимальный элемент:", 
                    "25%", "50%", "75%", "Максимальный элемент"] 
            name = name[0:len(analys)]
            analys.insert(0, "Свойства", name)
            for x in range(len(analys)):
                tree.insert("", x, iid=x, values=([analys[y][x] for y in tree["columns"]]))
            tree.pack(expand=1, fill='both')
            tree['show'] = 'headings'
            def clck2(analys):
                answer = mb.askokcancel(title="Сохранение", message="Сохранить базовый отчёт?")
                if answer == True:
                    db.save_excel(analys)
            butt2 = tki.Button(window2, text="Сохранить", command = lambda: clck2(analys),  padx="15", pady="6")
            butt2.pack(side="right")
            window2.mainloop()
            
            
        else:
            mb.showerror("Ошибка", "Выберите хотя бы один атрибут")
        
    c1 = tki.IntVar()
    c2 = tki.IntVar()
    c3 = tki.IntVar()
    c4 = tki.IntVar()
    c5 = tki.IntVar()
    c6 = tki.IntVar()
    c7 = tki.IntVar()
    c8 = tki.IntVar()
    c9 = tki.IntVar()
    c10 = tki.IntVar()
    c11 = tki.IntVar()
    c12 = tki.IntVar()
    
    che1 = tki.Checkbutton(window, text="ID", variable=c1, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che2 = tki.Checkbutton(window, text="Фамилия", variable=c2, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che3 = tki.Checkbutton(window, text="Имя", variable=c3, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che4 = tki.Checkbutton(window, text="Отчество", variable=c4, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che5 = tki.Checkbutton(window, text="Номер телефона", variable=c5, 
                           onvalue=1, offvalue=0, padx="15", pady="6")
    che6 = tki.Checkbutton(window, text="Дата вылета", variable=c6, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che7 = tki.Checkbutton(window, text="Название отеля", variable=c7, 
                           onvalue=1, offvalue=0, padx="15", pady="6")
    che8 = tki.Checkbutton(window, text="Статус оплаты", variable=c8, 
                           onvalue=1, offvalue=0, padx="15", pady="6")
    che9 = tki.Checkbutton(window, text="Стоимость", variable=c9, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che10 = tki.Checkbutton(window, text="Страна прибытия", variable=c10, 
                            onvalue=1, offvalue=0, padx="15", pady="6")
    che11 = tki.Checkbutton(window, text="Город прибытия", variable=c11, 
                            onvalue=1, offvalue=0, padx="15", pady="6")
    che12 = tki.Checkbutton(window, text="Количество звёзд", variable=c12, 
                            onvalue=1, offvalue=0, padx="15", pady="6")
    
    che1.pack()
    che2.pack()
    che3.pack()
    che4.pack()
    che5.pack()
    che6.pack()
    che7.pack()
    che8.pack()
    che9.pack()
    che10.pack()
    che11.pack()
    che12.pack()
    
    butt = tki.Button(window, text="Выбрать", command = clck,  padx="15", pady="6")
    butt.pack()
    
    
    window.mainloop()
    
def svodn_table():
    """
    Входные параметры : None
    Формирует сводную таблицу по выбранным параметрам и сохраняет её
    Выходные параметры: None
    Автор: Бригада 4
    """
    window = tki.Toplevel(root)
    window.geometry('370x300')
    window.title("Сводная таблица") 
    lbl = tki.Label(window, text="Выберите отчет, который необходимо сформировать,\nи параметр его формирования:", padx="15", pady="20")
    lbl.pack()
    
    def clck():
        if var.get() == 0:
            if combo0.get() == "Общая стоимость всех поездок":
                table = df4.pivot_table("Стоимость", index="Страна прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="sum")
            if combo0.get() == "Средняя стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Страна прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-")
            if combo0.get() == "Число поездок":
                table = df4.pivot_table("Стоимость", index="Страна прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="count")
            if combo0.get() == "Минимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Страна прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="min")
            if combo0.get() == "Максимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Страна прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="max")
        if var.get() == 1:
            if combo0.get() == "Общая стоимость всех поездок":
                table = df4.pivot_table("Стоимость", index="Город прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="sum")
            if combo0.get() == "Средняя стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Город прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-")
            if combo0.get() == "Число поездок":
                table = df4.pivot_table("Стоимость", index="Город прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="count")
            if combo0.get() == "Минимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Город прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="min")
            if combo0.get() == "Максимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Город прибытия", 
                                        columns="Количество звёзд", 
                                        fill_value="-", aggfunc="max")
        if var.get() == 2:
            if combo0.get() == "Общая стоимость всех поездок":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Страна прибытия", 
                                        fill_value="-", aggfunc="sum")
            if combo0.get() == "Средняя стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Страна прибытия", 
                                        fill_value="-")
            if combo0.get() == "Число поездок":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Страна прибытия", 
                                        fill_value="-", aggfunc="count")
            if combo0.get() == "Минимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Страна прибытия", 
                                        fill_value="-", aggfunc="min")
            if combo0.get() == "Максимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Страна прибытия", 
                                        fill_value="-", aggfunc="max")
        if var.get() == 3:
            if combo0.get() == "Общая стоимость всех поездок":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Город прибытия", 
                                        fill_value="-", aggfunc="sum")
            if combo0.get() == "Средняя стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Город прибытия", 
                                        fill_value="-")
            if combo0.get() == "Число поездок":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Город прибытия", 
                                        fill_value="-", aggfunc="count")
            if combo0.get() == "Минимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Город прибытия", 
                                        fill_value="-", aggfunc="min")
            if combo0.get() == "Максимальная стоимость поездки":
                table = df4.pivot_table("Стоимость", index="Статус оплаты", 
                                        columns="Город прибытия", 
                                        fill_value="-", aggfunc="max")
        window.destroy()
        window2 = tki.Toplevel(root)
        window2.geometry('800x350')
        window2.title("Сводная таблица") 
        tree = ttk.Treeview(window2)
        name = list(table.index)
        if var.get() == 0 or var.get() == 1:
            table.insert(0, 0, name)
        else: 
            table.insert(0, "", name)
        tree["columns"] = list(table)
        tree.column("#0", width=0, minwidth=0)
        for x in tree["columns"]:
            tree.column(x, width=75,minwidth=75)
        for x in tree["columns"]:
            tree.heading(x, text=x)
        for x in range(len(table)):
            if var.get() == 0 or var.get() == 1:
                tree.insert("", x, iid=x, values=([table[int(y)][x] for y in tree["columns"]]))
            else:
                tree.insert("", x, iid=x, values=([table[y][x] for y in tree["columns"]]))
        tree.pack(expand=1, fill='both')
        tree['show'] = 'headings'
        
        def clck2(table):
            answer = mb.askokcancel(title="Сохранение", message="Сохранить сводную таблицу?")
            if answer == True:
                db.save_excel(table)
                
        butt2 = tki.Button(window2, text="Сохранить", command = lambda: clck2(table),  padx="15", pady="6")
        butt2.pack(side="right")
        window2.mainloop()
    
    var = tki.IntVar()
    var.set(0)
    rad0 = tki.Radiobutton(window, text="Поездки в 1/2/3/4/5-звездные отели в каждой стране", 
                           variable=var, value=0, padx="15", pady="6")
    combo0 = Combobox(window, state='readonly')  
    combo0['values'] = ("Общая стоимость всех поездок", "Средняя стоимость поездки",
                        "Число поездок","Минимальная стоимость поездки", 
                        "Максимальная стоимость поездки")  
    combo0.current(1)
    combo0.pack()
    rad1 = tki.Radiobutton(window, text="Поездки в 1/2/3/4/5-звездные отели в каждом городе", 
                           variable=var, value=1, padx="15", pady="6")
    rad2 = tki.Radiobutton(window, text="Оплаченные и забронированные поездки в каждой стране", 
                           variable=var, value=2, padx="15", pady="6")
    rad3 = tki.Radiobutton(window, text="Оплаченные и забронированные поездки в каждом городе", 
                           variable=var, value=3, padx="15", pady="6")

    rad0.pack()
    rad1.pack()
    rad2.pack()
    rad3.pack()
    
    butt = tki.Button(window, text="Выбрать", command = clck,  padx="15", pady="6")
    butt.pack()
    
    window.mainloop()
    
def simple_report(cmb1, cmb2, sc1, sc2, br, op):
    """
    Входные параметры : cmb1, cmb2, sc1, sc2, br, op - переменные для выбранных
    пользователем ограничений
    Формирует и сохраняет таблицу с простым отчетом, получаемым путем 
    фильтрации по выбранным значениям
    Выходные параметры: None
    Автор: Бригада 4
    """
    filter_func(tree2, tree3, tree4,cmb1, cmb2, sc1, sc2, br, op)
    window = tki.Toplevel(root)
    window.geometry('370x520')
    window.title("Простой текстовый отчет") 
    lbl = tki.Label(window, text="Выберите столбцы, которые останутся в отчете:", padx="15", pady="15")
    lbl.pack()
    
    def clck():
        statb = pd.DataFrame()    
        if c1.get() == 1:
            statb["ID"] = df4["ID"]
        if c2.get() == 1:
            statb["Фамилия"] = df4["Фамилия"]
        if c3.get() == 1:
            statb["Имя"] = df4["Имя"]
        if c4.get() == 1:
            statb["Отчество"] = df4["Отчество"]
        if c5.get() == 1:
            statb["Номер телефона"] = df4["Номер телефона"]
        if c6.get() == 1:
            statb["Дата вылета"] = df4["Дата вылета"]
        if c7.get() == 1:
            statb["Название отеля"] = df4["Название отеля"]
        if c8.get() == 1:
            statb["Статус оплаты"] = df4["Статус оплаты"]
        if c9.get() == 1:
            statb["Стоимость"] = df4["Стоимость"]
        if c10.get() == 1:
            statb["Страна прибытия"] = df4["Страна прибытия"]
        if c11.get() == 1:
            statb["Город прибытия"] = df4["Город прибытия"]
        if c12.get() == 1:
            statb["Количество звёзд"] = df4["Количество звёзд"]

        window.destroy()
        if (c1.get() == 1 or c2.get() == 1 or c3.get() == 1 or c4.get() == 1 
            or c5.get() == 1 or c6.get() == 1 or c7.get() == 1 or c8.get() == 1
            or c9.get() == 1 or c10.get() == 1 or c11.get() == 1 or c12.get() == 1):
            new_base = pd.DataFrame(columns=list(statb))
            window2 = tki.Toplevel(root)
            window2.geometry('800x350')
            window2.title("Простой текстовый отчет") 
            tree = ttk.Treeview(window2)
            tree["columns"] = list(statb)
            tree.column("#0", width=0, minwidth=0)
            for x in tree["columns"]:
                tree.column(x, width=75,minwidth=75)
            for x in tree["columns"]:
                tree.heading(x, text=x)
            for x in range(len(statb)):
                if (df4["Стоимость"][x] >= from_price and df4["Стоимость"][x] <= to_price) \
                    and (df4["Количество звёзд"][x] >= from_stars and df4["Количество звёзд"][x] <= to_stars) \
                    and ((status == 1 and df4["Статус оплаты"][x] == "забронировано") \
                    or (status == 2 and df4["Статус оплаты"][x] == "оплачено") or status == 3):
                    tree.insert("", x, iid=x, values=([statb[y][x] for y in tree["columns"]]))
                    new_base.loc[x] = [statb[y][x] for y in tree["columns"]]
            tree.pack(expand=1, fill='both')
            tree['show'] = 'headings'
            def clck2(new_base):
                answer = mb.askokcancel(title="Сохранение", message="Сохранить отчёт?")
                if answer == True:
                    db.save_excel(new_base)
            butt2 = tki.Button(window2, text="Сохранить", command = lambda: clck2(new_base),  padx="15", pady="6")
            butt2.pack(side="right")
            window2.mainloop()
        else:
            mb.showerror("Ошибка", "Выберите хотя бы один атрибут")
    
    c1 = tki.IntVar()
    c2 = tki.IntVar()
    c3 = tki.IntVar()
    c4 = tki.IntVar()
    c5 = tki.IntVar()
    c6 = tki.IntVar()
    c7 = tki.IntVar()
    c8 = tki.IntVar()
    c9 = tki.IntVar()
    c10 = tki.IntVar()
    c11 = tki.IntVar()
    c12 = tki.IntVar()
    
    che1 = tki.Checkbutton(window, text="ID", variable=c1, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che2 = tki.Checkbutton(window, text="Фамилия", variable=c2, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che3 = tki.Checkbutton(window, text="Имя", variable=c3, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che4 = tki.Checkbutton(window, text="Отчество", variable=c4, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che5 = tki.Checkbutton(window, text="Номер телефона", variable=c5, 
                           onvalue=1, offvalue=0, padx="15", pady="6")
    che6 = tki.Checkbutton(window, text="Дата вылета", variable=c6, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che7 = tki.Checkbutton(window, text="Название отеля", variable=c7, 
                           onvalue=1, offvalue=0, padx="15", pady="6")
    che8 = tki.Checkbutton(window, text="Статус оплаты", variable=c8, 
                           onvalue=1, offvalue=0, padx="15", pady="6")
    che9 = tki.Checkbutton(window, text="Стоимость", variable=c9, onvalue=1, 
                           offvalue=0, padx="15", pady="6")
    che10 = tki.Checkbutton(window, text="Страна прибытия", variable=c10, 
                            onvalue=1, offvalue=0, padx="15", pady="6")
    che11 = tki.Checkbutton(window, text="Город прибытия", variable=c11, 
                            onvalue=1, offvalue=0, padx="15", pady="6")
    che12 = tki.Checkbutton(window, text="Количество звёзд", variable=c12, 
                            onvalue=1, offvalue=0, padx="15", pady="6")
    
    che1.pack()
    che2.pack()
    che3.pack()
    che4.pack()
    che5.pack()
    che6.pack()
    che7.pack()
    che8.pack()
    che9.pack()
    che10.pack()
    che11.pack()
    che12.pack()
    
    butt = tki.Button(window, text="Выбрать", command = clck,  padx="15", pady="6")
    butt.pack()
    
    window.mainloop()     


from_stars, to_stars, from_price, to_price, status = 0, 5, 0, 3000000, 3
menu = tki.Menu(root)
item_f = tki.Menu(menu, tearoff=0)
item_f.add_command(label='Создать новую базу данных', command = new_bases)
item_f.add_command(label='Сохранить', command = lambda : db.safe_base(df1, df2, df3))
item_f.add_command(label='Сохранить как', command = lambda : db.save_base_like(df1, df2, df3))
menu.add_cascade(label='Таблица', menu=item_f)
    
item_a = tki.Menu(menu, tearoff=0)
item_a.add_command(label='Кластеризованная столбчатая диаграмма', command = lambda: Graf1(df1))
item_a.add_command(label='Категоризированная гистограмма', command = lambda: Graf2(df3))
item_a.add_command(label='Категоризированная диаграмма Бокса-Вискер', command = lambda: Graf3(df4))
item_a.add_command(label='Категоризированная диаграмма рассеивания', command = lambda: Graf4(df4))
item_a.add_command(label='Сводная таблица', command = lambda: svodn_table())
item_a.add_command(label='Базовая статистика', command = lambda: basestat(df4))
menu.add_cascade(label='Анализ', menu=item_a)
    
item_p = tki.Menu(menu, tearoff=0)
item_p.add_command(label='Найти',command=find)
menu.add_cascade(label='Поиск', menu=item_p)
    
item_i = tki.Menu(menu, tearoff=0)
item_i.add_command(label='О разработчиках', command=lambda: \
                       show_info(root))
menu.add_cascade(label='Справка', menu=item_i)
    
root.config(menu=menu)
    
box = tki.Canvas(root, width=900, height=200)
box.pack()
    
box.create_line(10, 10, 10, 82, fill='grey', width=0.5)
box.create_line(10, 82, 275, 82, fill='grey', width=0.5)
box.create_line(275, 82, 275, 10, fill='grey', width=0.5)
box.create_line(10, 10, 275, 10, fill='grey', width=0.5)
lbl1 = tki.Label(root, text='Редактирование', fg="grey")
lbl1.place(x=14, y=0)
    

tab_control = ttk.Notebook(root, height='700', width='900')

tab_clients = ttk.Frame(tab_control)
tab_trips = ttk.Frame(tab_control)
tab_hotels = ttk.Frame(tab_control)
tab_all = ttk.Frame(tab_control)
    
tab_control.add(tab_clients, text='Клиенты')
tree1 = ttk.Treeview(tab_clients)
tree1 = show_table_clients(tree1, df1)
    
tab_control.add(tab_trips, text='Поездки')
tree2 = ttk.Treeview(tab_trips)
tree2 = show_table_trips(tree2, df2)
    
tab_control.add(tab_hotels, text='Отели')
tree3 = ttk.Treeview(tab_hotels)
tree3 = show_table_hotels(tree3, df3) 
    
tab_control.add(tab_all, text='Общая таблица')
tree4 = ttk.Treeview(tab_all)
df4 = db.make_table4(df1, df2, df3)
tree4 = show_table_all(tree4, df4) 
    
tab_control.place(relheight=1.0, relwidth=1.0, relx=0.0, rely=0.289)

box.create_line(285, 10, 285, 129, fill='grey', width=0.5)
box.create_line(285, 129, 890, 129, fill='grey', width=0.5)
box.create_line(285, 10, 890, 10, fill='grey', width=0.5)
box.create_line(890, 10, 890, 129, fill='grey', width=0.5)
lbl2 = tki.Label(root, text='Фильтры', fg="grey")
lbl2.place(x=290, y=0)

lbl3 = tki.Label(root, text="Количество звезд  от")
lbl3.place(x=295, y=17)
combo1 = ttk.Combobox(root)  
combo1['values'] = ("1", "2", "3", "4", "5")  
combo1.current(0)  
combo1.place(x=420, y=16)
lbl4 = tki.Label(root, text="до")
lbl4.place(x=570, y=17)
combo2 = ttk.Combobox(root)  
combo2['values'] = ("1", "2", "3", "4", "5")  
combo2.current(4)  
combo2.place(x=595, y=16)

lbl5 = tki.Label(root, text="Стоимость от")
lbl5.place(x=295, y=55)
sca1 = tki.Scale(root, orient="horizontal", length=190, from_=0, to=1500000, 
                 tickinterval=500000, resolution=10000)
sca1.place(x=376, y=37)
lbl5 = tki.Label(root, text="до")
lbl5.place(x=569, y=55)
sca2 = tki.Scale(root, orient="horizontal", length=190, from_=0, to=1500000, 
                 tickinterval=500000, resolution=10000)
sca2.place(x=588, y=37)
sca2.set(1500000)

bron = tki.IntVar()
opl = tki.IntVar()
check1 = tki.Checkbutton(root, text="Забронировано", variable=bron, onvalue=1, 
                           offvalue=0)
check2 = tki.Checkbutton(root, text="Оплачено", variable=opl, onvalue=1, 
                           offvalue=0)
bron.set(1)
opl.set(1)
check1.place(x=590, y=100)
check2.place(x=713, y=100)

filter_button = tki.Button(root, text="Применить", command = lambda: \
                           filter_func(tree2, tree3, tree4, combo1.get(), 
                                       combo2.get(), sca1.get(), sca2.get(),
                                       bron.get(), opl.get()))
filter_button.place(x=805, y=35)

filt_save_button = tki.Button(root, text="Экспорт", command = lambda: \
                           simple_report(combo1.get(), combo2.get(), 
                           sca1.get(), sca2.get(), bron.get(), opl.get()))
filt_save_button.place(x=822, y=80)                          

edit_button = tki.Button(root, text="Редактировать", command = lambda: change(tree1, tree2, tree3, tree4))
edit_button.place(x=113, y=50)
    
new_client_button = tki.Button(root, text="Новый клиент", command = lambda: add_client(tree1, tree4))
new_client_button.place(x=15, y=20) 
    
new_trip_button = tki.Button(root, text="Новая поездка", command = lambda: add_trip(tree2, tree4))
new_trip_button.place(x=15, y=50)  
    
new_hotel_button = tki.Button(root, text="Новый отель", command = lambda: add_hotel(tree3, tree4))
new_hotel_button.place(x=113, y=20)
  
delete_button = tki.Button(root, text="Удалить", command = lambda: delete(tree1, tree2, tree3, tree4))
delete_button.place(x=212, y=50)

root.mainloop()
    
