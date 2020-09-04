# -*- coding: utf-8 -*-

import re
import csv
import gc
import tarfile

"""Конфигурация"""

archive_name = 'py150.tar.gz'
file_names_for_load = ['python100k_train.json'] #

file_names_for_load = ['python50k_eval.json']

file_names_for_load = ['githab_snippets.json']

"""# Загрузка данных"""

# Распаковка архива с датасетами
with tarfile.open(archive_name) as tar:
    tar.extractall()

# Функция для загрузки данных из файлов
def load_data_from_files(file_name, verbose=0):
    data = []
    with open(file_name, 'r') as json_file:
        for line in json_file:
            data.append(line)
    if verbose >= 1:
         print('Примеров загружено из файла: ' + str(len(data)))
    return data

data = load_data_from_files(file_names_for_load)

"""# Обработка загруженных данных"""

def data_preparation(data):
    progs_vec_ast = []

    # Преобразование строки AST вектора в лист с нодами
    for line in data:
        progs_vec_ast.append(line.split('},{'))

    del data
    gc.collect()

    functions = []

    # Выбор функций из программ
    for pva in progs_vec_ast:
        for i,node in enumerate(pva):
            if 'FunctionDef' in node:
                try:
                    func_name = re.search(r'\"value\":\"([A-z0-9]*)\"', node).group(1)
                    last_index_child = int(re.search(r'\"children\":\[(([0-9]*),)*?([0-9]*)]', node).group(3))
                except:
                    #print('Missed: ' + node)
                    continue
                func_vec_ast = pva[i:last_index_child]
                functions.append([func_name, func_vec_ast])

    del progs_vec_ast
    gc.collect()

    ''' Отчистка нодов функций от лишней информации
    Приведение данных к виду:
                                list[0] - название функции
                                list[1] - [тип нода, значение_нода/None]
 '''
    for i,func in enumerate(functions):
        for j,node in enumerate(func[1]):
            try:
                ntype =  re.search(r'\"type\":\"([A-z]*)\"',node)[1]
            except:
                ntype = '<MSD>'
            try:
                nvalue = re.search(r'\"value\":\"(.*)\"',node)[1]
            except:
                nvalue = None
            functions[i][1][j] = [ntype, nvalue]

    gc.collect()

    print('Всего функций в  наборе: ' + str(len(functions)))

    return functions

progs_vec_ast = []

# Преобразование строки AST вектора в лист с нодами
for line in data:
    progs_vec_ast.append(line.split('},{'))

del data
gc.collect()

progs_vec_ast[2]

functions = []

# Выбор функций из программ
for pva in progs_vec_ast:
    for i,node in enumerate(pva):
        if 'FunctionDef' in node:
            try:
                func_name = re.search(r'\"value\":\"([A-z0-9]*)\"', node).group(1)
                last_index_child = int(re.search(r'\"children\":\[(([0-9]*),)*?([0-9]*)]', node).group(3))
            except:
                #print('Missed: ' + node)
                continue
            func_vec_ast = pva[i:last_index_child]
            functions.append([func_name, func_vec_ast])

del progs_vec_ast
gc.collect()

functions[2]

''' Отчистка нодов функций от лишней информации
    Приведение данных к виду:
                                list[0] - название функции
                                list[1] - [тип нода, значение_нода/None]
 '''
for i,func in enumerate(functions):
    for j,node in enumerate(func[1]):
        try:
            ntype =  re.search(r'\"type\":\"([A-z]*)\"',node)[1]
        except:
            ntype = '<MSD>'
        try:
            nvalue = re.search(r'\"value\":\"(.*)\"',node)[1]
        except:
            nvalue = None
        functions[i][1][j] = [ntype, nvalue]

gc.collect()

"""Выбор функций для обучения"""

'Всего функций в  наборе: ' + str(len(functions))

func_names = {}

# Составление счётчика словаря по всем названиям функций
for func in functions:
    if func[0] in func_names:
        func_names[func[0]] += 1
    else:
        func_names[func[0]] = 1

threshold = 300 # порог отбора функций по счётчику

func_names = [(name, score) for name, score in func_names.items() if score > threshold]
func_names.sort(key=lambda x: x[1], reverse=True)

f'Количество классов, где есть более {threshold} примеров функций: ' + str(len(func_names))

func_names

# Избавлсяемся от счётной информации и оставляем только названия функций
func_names = [tp[0] for tp in func_names]

# --Сохранить названия функций в файл, чтобы использовать при выборе функций в тестовой выборке--
with open('func_names.txt', 'w') as fn_file:
    fn_file.write(','.join(func_names))

# --Загрузка имен функций из файла для фильтрации тестовой выборки
with open('func_names.txt', 'r') as fn_file:
    func_names = fn_file.readline().split(',')

# Функция для удаления элементов списка по значению
def remove_items(lst, items):
    for item in items:
        try:
            lst.remove(item)
        except ValueError:
            print(f'VelueError: \'{item}\' not in list')
    return lst

# Удаляем из списка функций названия функций, которые не будут использоваться при обучении
func_names = remove_items(func_names, ['__init__', 'main', 'run', '__call__',
                                       '__iter__', 'f', '__enter__','__exit__',
                                       '__new__', '__hash__', '__ne__', '__del__',
                                       '__lt__', '__nonzero__', 'func', 'foo', 'fn', 'cb', 'g', '_run'])

func_names[:5]

functions[0]

functions_train = []

# Приведение названий у одинаковых по смыслу функций к единому
for i,func in enumerate(functions):
    if func[0] in func_names:
        if func[0] in '__repr__str__':
            functions[i][0] = 'to_string'
        elif func[0] == 'setUp':
            functions[i][0] = 'setup'
        functions_train.append(functions[i])

func_names = remove_items(func_names, ['__repr__', '__str__', 'setUp'])

print('Кол-во функций для обучения: ' + str(len(functions_train)))
functions_train[100]

ave = sum(len(nodes[1]) for nodes in functions_train) / len(functions_train)
print('Средняя длина вектора АСД: ' + str(ave))

"""Выбор альтернативы использования название нода или значения нода"""

func_names = {}
for func in functions_train:
    if func[0] in func_names:
        func_names[func[0]] += 1
    else:
        func_names[func[0]] = 1
print('Уникальных функций в наборе: ', len(func_names))

unic_values = {}
for func in functions_train:
    for node in func[1]:
        if node[1] in unic_values:
            unic_values[node[1]] += 1
        else:
            unic_values[node[1]] = 1
print('Уникальных значений нодов в наборе: ', len(unic_values))

max_values_dict = 9000

# Ограничение размера словаря уникальных значений нодов
unic_values = [(name, score) for name, score in unic_values.items()]
unic_values.sort(key=lambda x: x[1], reverse=True)
unic_values = unic_values[:max_values_dict]
unic_values = [x[0] for x in unic_values]
del unic_values[0] # del None-value

# --Сохранить уникальных значений в файл, чтобы использовать при выборе функций в тестовой выборке--
with open('values_dict.txt', 'w') as vn_file:
    vn_file.write(','.join(unic_values))

# --Загрузка имен функций из файла для фильтрации тестовой выборки
with open('values_dict.txt', 'r') as vn_file:
    unic_values = vn_file.readline().split(',')

unic_values[:10]

# Выбор использования значения нода или тип с связи со словарем

for i,func in enumerate(functions_train):
    for j,node in enumerate(func[1]):
        if node[1]:
            if node[1] in unic_values:
                functions_train[i][1][j] = node[1]
            else:
                functions_train[i][1][j] = node[0]
        else:
            functions_train[i][1][j] = node[0]

def filter_nodes(functions_train):
    for i,func in enumerate(functions_train):
        for j,node in enumerate(func[1]):
            if node[1]:
                if node[1] in unic_values:
                    functions_train[i][1][j] = node[1]
                else:
                    functions_train[i][1][j] = node[0]
            else:
                functions_train[i][1][j] = node[0]

    gc.collect()

    # Удаление названия функций из АСД вектора
    for i in range(len(functions_train)):
        try:
            del functions_train[i][1][0]
        except IndexError:
            print(i, ' : ', functions_train[i])

gc.collect()

# Удаление названия функций из АСД вектора
    for i in range(len(functions_train)):
            del functions_train[i][1][0]

functions_train[5000]

"""# Подгатовка сниппетов"""

filename_snippets = 'github_s.json'
filename_token_dict = 'dictionary_9107.txt'
filename_class_dict = 'dictionary_111.txt'

snippets = load_data_from_files(filename_snippets)
snippets = data_preparation(snippets)


# --Загрузка уникальных имен токенов из файла для фильтрации тестовой выборки
with open(filename_token_dict, 'r') as vn_file:
    unic_values = vn_file.readline().split(',')

# --Загрузка имен функций из файла для фильтрации тестовой выборки
with open(filename_class_dict, 'r') as fn_file:
    func_names = fn_file.readline().split(',')

filter_nodes(snippets)

del snippets[2]
snippets

funcs_to_file(snippets)

"""# Сохранение готовых данных в файлы

Сохранение всех данных в один файл
"""

def funcs_to_file(functions_train):
    with open(f'snip_d{max_values_dict}_t{threshold}.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'ast'])

        for func in functions_train:
                writer.writerow({'name':func[0], 'ast':','.join(func[1])})

"""Разделение на тренировочную и тестовую выборку и сохранение в файлы"""

# precent ratio - параметр деления данных (70% - train | 30% - test)
p_ratio = 0.7

with open('train_m.csv', 'w') as f_train:
    with open('test_m.csv', 'w') as f_test:

        delim_num = int( len(functions_train) * p_ratio )

        train_writer = csv.DictWriter(f_train, fieldnames=['name', 'ast'])
        test_writer = csv.DictWriter(f_test, fieldnames=['name', 'ast'])

        for i,func in enumerate(functions_train):
            if delim_num > i:
                train_writer.writerow({'name':func[0], 'ast':','.join(func[1])})
            else:
                test_writer.writerow({'name':func[0], 'ast':','.join(func[1])})
