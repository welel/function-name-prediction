import csv
import random



def shuffle_file_lines(
        filename: str,
        header: bool=False,
        new_file: bool=False):
    '''
    Принимает название файла и перемешивает строки в файле.
    Если header = True, то пропускает первую строку.
    Если new_file = Ture, то записывает результат в новый файл.
    '''
    with open(filename, 'r') as file:
        if header:
            header = file.readline()
        rows = file.read().split()
    random.shuffle(rows)
    if new_file:
        filename = 'shuffled_' + filename
    with open(filename, 'w') as file:
        if header:
            file.write(header)
        file.write('\n'.join(rows))


def merge_files(filename1: str, filename2: str, newfilename: str):
    '''
    Получает на вход 3 названия файлов, объединяет два первых и
    записывает результат в третий.
    '''
    rows = []
    with open(filename1, 'r') as file1:
        rows.extend(file1.read().split())
    with open(filename2, 'r') as file2:
        rows.extend(file2.read().split())
    with open(newfilename, 'w') as newfile:
        newfile.write('\n'.join(rows))


def split_file(filename: str, split_ratio: float):
    '''
    Принимает на вход название файла и коэффициент деления, затем
    делит файл по коэффициенту на два новых.
    '''
    with open(filename, 'r') as mfile:
        rows = mfile.read().split()

    pivot = int(len(rows) * split_ratio)
    rows_iter = enumerate(rows)

    with open(f'train_{filename}', 'w') as file1:
        i = 0
        while i <= pivot:
            i, row = next(rows_iter)
            file1.write(row + '\n')

    with open(f'test_{filename}', 'w') as file2:
        for i, row in rows_iter:
            file2.write(row + '\n')
