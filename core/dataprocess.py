from typing import Union
import csv
import json
import functools
import time



def timer(func):
    '''Декоратор для оценки времени работы функции.'''
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f'[{func.__name__}] execution time: ' \
                f'{elapsed_time:0.4f} seconds\n')
        return value
    return wrapper_timer


def append_functions_in_json(path: str, functions: list):
    '''
    Функция принимает на вход название json файла и последовательность
    функций, и добавляет функции в конец файла.
    '''
    with open(path, 'a') as json_file:
        for function in functions:
            json.dump(function, json_file)
            json_file.write('\n')


def get_funcs_from_module(module: list) -> list:
    '''
    Выбор слайсов, относящихся к функциям и возврат списка слайсов
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


def read_portion_data(path: str,
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
    with open(path, 'r') as file:
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
    регистру и удаляет двойное подчеркивание из названий.
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


def load_functions_from_json(path: str) -> list:
    '''Загрузка датасета с функциями из json файла.'''
    functions = []
    with open(path, 'r') as json_file:
        for line in json_file:
            functions.append(json.loads(line))
    return functions


def dataset_save_to_csv(path: str, dataset: list):
    '''
    Сохраняет готовый датасет с функциями в .csv файл по полям:
    [метка функции (ее название)], [последовательность узлов функции].
    '''
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'ast'])
        for data in dataset:
                writer.writerow({'name': data[0], 
                    'ast': ','.join(data[1]).replace('\0', ' ').replace('\n', ' ')})
                

def lzip(*iterables):
    '''
    Модификация встроенной функции в Python zip(),
    которая генерирует не tuple(), а list().
    '''
    sentinel = object()
    iterators = [iter(it) for it in iterables]
    while iterators:
        result = []
        for it in iterators:
            elem = next(it, sentinel)
            if elem is sentinel:
                return
            result.append(elem)
        yield list(result)


@timer
def count_file_lines(path: str) -> int:
    '''Подсчет количества строк в файле.'''
    with open(path, 'r') as file:
        return sum(1 for line in file)


@timer
def get_uniq_dictcounters(path: str, verbose: bool=False):
    '''
    Функция получает путь к файлу .json с функциями и
    считает уникальные значения имен функций и узлов функций
    в два отдельных словаря-счетчика. (Файл читается порционно).
    
    Словарь-счётчик:
        dict -> {item: amount, item2: amount2, ...}
    '''
    uniq_names = {} # счётичик уникальных имен функций
    uniq_values = {} # # счётичик уникальных значений узлов
    
    batch_size = 1000 # размер порции (1000 для ОЗУ объемом 4 Гб)
    pos = 0 # начальная позиция чтения файла
    counter = 0 # счётчик обработанных функций

    # Порционный перебор функций из датасета
    functions, pos = read_portion_data(path, pos, 1)
    while functions:
        functions, pos = read_portion_data(path, pos, batch_size)
        
        counter += len(functions) 
            
        # Добавить имена в словарь подсчета уникальных имен функций
        for func in functions:
            func = json.loads(func)
            uniq_names[func[0]['value']] = uniq_names.get(func[0]['value'], 0) + 1
            # Добавить имена в словарь подсчета уникальных значений узлов
            for node in func:
                if 'value' in node:
                    uniq_values[node['value']] = uniq_values.get(node['value'], 0) + 1
                
        if verbose:
            print('Функций обработано: ', counter, 
                    '| Ун. имен', len(uniq_names), 
                    '| Ун. знач.:', len(uniq_values)
                 )
    return uniq_names, uniq_values


def dictcounter_to_json(dictcounter: dict, path: str):
    '''Запись словаря-счетчика в файл json.'''
    with open(path, 'w') as json_file:
        json.dump(dictcounter, json_file)


def dictcounter_from_json(path: str):
    '''Чтение словаря-счетчика из файла json.'''
    with open(path, 'r') as json_file:
        return json.load(json_file)


def cut_dictcounter(dictcounter : dict, thresholder : int) -> dict:
    '''
    Удаляет ключи словаря-счетчика по заданному порогу вхождения.
    Если счетчик ключа меньше порога, то такой ключ удаляется.
    '''
    new_dict = {}
    for key, counter in dictcounter.items():
        if counter > thresholder:
            new_dict[key] = counter
    return new_dict


@timer
def filter_functions(funcs_path: str,
                        filtered_funcs_path: str,
                        names: set) -> int:
    '''
    Отфильтровывает функции по именам, не входящим в заданное множество.
    
    Takes:
        * funcs_path: str (путь к json файлу с функциями)
        * filtered_funcs_path: str (путь куда записать отфильтрованные
                                    функции)
        * names: set (множество имен функций)
    Returns:
        * int (количество функций после фильтрации)
    '''
    batch_size = 1000 # Для ОЗУ 8 гигабайт.
    pos = 0
    filtered_func_number = 0

    functions, pos = read_portion_data(funcs_path, pos, 1)
    while functions:
        functions, pos = read_portion_data(funcs_path, pos, batch_size)
        
        for i,function in enumerate(functions):
            try: # Решает проблему ошибки делиметра
                functions[i] = json.loads(functions[i])
            except json.JSONDecodeError as e:
                print(e)
                functions[i] = functions[i-1]
                continue

        filterd_functions = filter_functions_name(functions, names)
        filtered_func_number += len(filterd_functions)
        
        append_functions_in_json(
            filtered_funcs_path,
            filterd_functions
        )
    return filtered_func_number
