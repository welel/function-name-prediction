from typing import Union
import csv
import json


def append_functions_in_json(file_name: str, functions: list):
    '''
    Функция принимает на вход назване json файла и последовательность
    функций, и добавляет функции в конец файла.
    '''
    with open(file_name, 'a') as json_file:
        for function in functions:
            json.dump(function, json_file)
            json_file.write('\n')


def get_funcs_from_module(module: list) -> list:
    '''
    Выбор слайсов относящихся к функциям и возрат списка слайсов
    этих функций.
        * module: list  - последовательность узлов программы (модуля)
        * module[i] -> node
        * node -> {'type':str, 'children':list, 'value':str}
        * node['children'][i] -> int
    '''
    functions = []
    i = 0
    while i < len(module):
        if module[i]['type'] == 'FunctionDef':
            last_child = module[i]['children'][-1]
            functions.append(module[i:last_child])
            i = last_child+1
        else:
            i+=1
    return functions


def read_portion_data(file_name: str,
                      pos: int,
                      num_lines: int
                      ) -> Union[list, int]:
    '''
    Загрузка порции данных из файла, читая файл с определенной
    позиции (pos) и определенное количество строк (lines).

    Returns:
        * data [list]
        * last_position [int]
    '''
    data = []
    with open(file_name, 'r') as file:
        file.seek(pos)
        line = file.readline()
        while line and num_lines > 0:
            data.append(line)
            line = file.readline()
            num_lines -= 1
        return data, file.tell()


def simplify_functions(functions: list) -> list:
    '''
    Приводит названия полученных функций и значения ее узлов к нижнему
    регистру и удаляет двойное подчеркиваение из назывний.
    '''
    for i,function in enumerate(functions):
        for j,n in enumerate(function):
            if 'value' in functions[i][j]:
                functions[i][j]['value'] = functions[i][j]['value'].lower().replace('__', '')
    return functions


def filter_functions_name(functions: list, names: set) -> list:
    '''
    Фильтрует функции по полученному на вход списку имен функций,
    которые надо оставить.

    Returns:
        * functions [list]
    '''
    return list(filter(lambda func: func[0]['value'] in names, functions))


def load_functions_from_json(file_name: str) -> list:
    '''Загрузка датасета с функциями из json файла.'''
    functions = []
    with open(file_name, 'r') as json_file:
        for line in json_file:
            functions.append(json.loads(line))
    return functions


def dataset_save_to_csv(file_name: str, dataset: list):
    '''
    Сохраняет готовый датасет с функциями в .csv файл по полям:
    [метка функции (ее название)], [последовательность узлов функции].
    '''
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'ast'])
        for data in dataset:
                writer.writerow({'name': data[0], 'ast': ','.join(data[1]).replace('\n', '')})
                
