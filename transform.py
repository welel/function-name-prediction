from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


class Converter(object):
    '''
    Класс Converter хранит словари токенов и меток, а также предоставляет
    методы для конвертации данных с помощью хранимых словарей.
    '''
    def __init__(self, sequence: list):
        '''
        Инициализирует словари по уникальным значениям полученной
        последовательности
        '''
        self.item_index_dict = {}
        self.index_item_dict = {}
        for index, item in enumerate(set(sequence)):
            self.item_index_dict[item] = index
            self.index_item_dict[index] = item
        self.item_index_dict['<MSD>'] = len(self.item_index_dict)
        self.index_item_dict[len(self.index_item_dict)] = '<MSD>'
        assert len(self.item_index_dict) == len(self.index_item_dict)

    def item_to_index(self, item: str) -> int:
        '''Получает на вход значение и возвращает его индекс'''
        try:
            index = self.item_index_dict[item]
        except KeyError:
            index = self.item_index_dict['<MSD>']
        return index

    def index_to_item(self, index: int) -> str:
        '''Получает на вход индекс и возвращает соответствущее значение'''
        return self.index_item_dict[index]

    def __len__(self):
        '''Длина равна общему количеству отображений'''
        return len(self.item_index_dict)

    def to_file(self):
        '''Сохраняет словарь с отображениями в файл'''
        with open('dictionary_'+ str(len(self)) + '.txt', 'w') as file:
            for item in self.item_index_dict:
                file.write(item + ',' + str(self.item_to_index(item)) + '\n')

    def build_converters(x_train, x_test, y_train, y_test, verbose=0):
        '''
        Создает конвертеры для тренировочного и тестового датасета.

        Takes:
            * x_train: list (тренировочные данные для обучения)
            * y_train: list (метки для валидации предсказания для
                            тренировочной выборки)
            * x_test: list (тестовые данные для проверки модели)
            * y_test: list (метки для валидации предсказания для
                            тестовой выборки)
            * verbose: int (отвечает за вывод информации о
                            конвертерах в stdout)
        Returns:
            * converter_data: Converter (конвертер для данных)
            * converter_labels: Converter (конвертер для меток)
        '''
        sequence = ','.join(x_train).split(',')
        sequence.extend(','.join(x_test).split(','))
        converter_data = Converter(sequence)

        sequence = list(y_test)
        sequence.extend(y_test)
        converter_labels = Converter(sequence)

        if verbose >= 1:
            print('Уникальных токенов: ' + str(len(converter_data)))
            print('Уникальных классов: ' + str(len(converter_labels)), end='\n\n')
        return converter_data, converter_labels


    def data_to_digital(self, sequence: list, verbose=0) -> list:
        '''
        Совершает преобразование последовательности токенов к цифровому виду.
        Использует для преобразования словарь отображения item_index_dict.
        Takes:
            * sequence: List[str] (последовательность токенов)
        Returns:
            * sequence: List[int] (последовательность отображений токенов)
        '''
        if len(sequence[0].split(',')) == 1:
            for index, item in enumerate(sequence):
                sequence[index] = self.item_to_index(item)
        else:
            for index, row in enumerate(sequence):
                row = row.split(',')
                sequence[index] = []
                for item in row:
                    sequence[index].append(self.item_to_index(item))
        if verbose >= 1:
            print('Пример данных после data_to_digit: ')
            print(sequence[0])
        return sequence


def to_same_length(sequence: list,
                   maxlen: int,
                   reverse: bool=False,
                   verbose: int=0) -> list:
    '''
    Приводит последовательности к одной длине, обрезая длинные
    последовательности и дополняя нулями в начале короткие.
    '''
    if reverse:
        for i,snippet in enumerate(sequence):
            sequence[i] = snippet[::-1]

    for i,row in enumerate(sequence):
        if len(row) > maxlen:
            sequence[i] = row[0:maxlen]

    sequence = pad_sequences(sequence, maxlen=maxlen)

    if verbose >= 1:
        print('Пример данных выборки после приведения к одной длине:')
        print(sequence[0],end='\n\n')
    return sequence


def vectorize_sequences(classes: list, dimension: int, verbose=0) -> list:
    '''
    Преобразование меток (классов) в One Hot Encoding формат.

    Takes:
        * classes: list (метки для валидации)
        * dimension: int (количество уникальных меток)
        * verbose: int (отвечает за вывод информации в stdout)
    Returns:
        * classes_ohe: list (метки преобразованные в One Hot Encoding формат)
    '''
    classes_ohe = np.zeros((len(classes), dimension))
    for i, sequence in enumerate(classes):
        classes_ohe[i, classes] = 1.

    if verbose >= 1:
        print('Пример метки выборки:')
        print(classes_ohe[0], end='\n\n')
    return classes_ohe