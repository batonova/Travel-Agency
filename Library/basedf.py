# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Эта библиотека содержит набор функций для работы с базой данных

Авторы: Анисимов А., Батонова О., Батрокова Е. (Бригада 4)
"""
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import pandas as pd
import os

WD = os.getcwd()
os.chdir(WD+"/.."+"/data")



def open_table1():
    """
    Входные параметры : None
    Считывает данные базы данных из двоичного формата pickle
    Выходные параметры df1-dataFrame «Клиенты»
    Автор: Бригада 4
    """
    df1 = pd.read_pickle('clients.pkl')
    return df1
def open_table2():
    """
    Входные параметры : None
    Считывает данные базы данных из двоичного формата pickle
    Выходные параметры df2-dataFrame «Поездки»
    Автор: Бригада 4
    """
    df2 = pd.read_pickle('trips.pkl')
    return df2
def open_table3():
    """
    Входные параметры : None
    Считывает данные базы данных из двоичного формата pickle
    Выходные параметры df3-dataFrame «Отели»
    Автор: Бригада 4
    """
    df3 = pd.read_pickle('hotels.pkl')
    return df3

def make_table4(df1, df2, df3):
    """
    Входные параметры : df1, df2, df3-(dataFrame) данные из трёх таблиц в третьей нормальной форме
    Создаёт общую таблицу 
    Выходные параметры df4-dataFrame общая таблица
    Автор: Бригада 4
    """
    df4 = pd.merge(df1, pd.merge(df2, df3, on = ['Название отеля']), on = 'ID') 
    return df4

def safe_base(df1, df2, df3):
    """
    Входные параметры : df1, df2, df3-(dataFrame) данные из трёх таблиц в третьей нормальной форме
    Сохраняет базы данных в двоичном формате pickle
    Выходные параметры: None
    Автор: Бригада 4
    """
    df1.to_pickle('clients.pkl')
    df2.to_pickle('trips.pkl')
    df3.to_pickle('hotels.pkl')
    
def save_base_like(df1, df2, df3):
    """
    Входные параметры : df1, df2, df3-(dataFrame) данные из трёх таблиц в третьей нормальной форме
    Сохраняет базы данных в двоичном формате pickle по пути, выбранному пользователем
    Выходные параметры: None
    Автор: Бригада 4
    """
    answer = mb.askokcancel(title="Сохранение", message="Сохранить базу клиентов?")
    if answer == True:
        name1 = fd.asksaveasfilename(defaultextension='.pickle')
        f1 = open(name1, 'wb')
        df1.to_pickle(name1)
        f1.close()
    
    answer = mb.askokcancel(title="Сохранение", message="Сохранить базу поездок?")
    if answer == True:    
        name2 = fd.asksaveasfilename(defaultextension='.pickle')
        f2 = open(name2, 'wb')
        df2.to_pickle(name2)
        f2.close()
    
    answer = mb.askokcancel(title="Сохранение", message="Сохранить базу отелей?")
    if answer == True:
        name3 = fd.asksaveasfilename(defaultextension='.pickle')
        f3 = open(name3, 'wb')
        df3.to_pickle(name3)
        f3.close()
        
def save_excel(df):
    """
    Входные параметры : df - база данных (DataFrame)
    Сохраняет базу данных из DataFrame в Exel по пути, выбранному пользователем
    Выходные параметры: None
    Автор: Бригада 4
    """
    name = fd.asksaveasfilename(defaultextension='.xlsx')
    if name:
        df.to_excel(name, index=False)
    
    