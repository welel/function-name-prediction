import csv
from transform import Converter, to_same_length, vectorize_sequences


def load_data(train_file_name: str, test_file_name: str, verbose: int=0):
    '''
    Принимает на вход названия тренировочного и валидационного файлов,
    возращает 4 списка, два с метками и два с узлами.

    Returns:
        * x_train: list (тренировочные данные для обучения)
        * y_train: list (метки для валидации предсказания
                        для тренировочной выборки)
        * x_test: list (тестовые данные для проверки модели)
        * y_test: list (метки для валидации предсказания
                        для тестовой выборки)
    '''
    x_train, y_train, x_test, y_test = [], [], [], []

    with open(train_file_name, 'r') as tfile:
        r = csv.reader(tfile)
        for row in r:
            y_train.append(row[0])
            x_train.append(row[1])

    with open(test_file_name, 'r') as efile:
        r = csv.reader(efile)
        for row in r:
            y_test.append(row[0])
            x_test.append(row[1])

    if verbose >= 1:
        print('load_data: Примеров в обучающей выбоке:', str(len(x_train)))
        print('load_data: Примеров в тестовой выбоке:', str(len(x_test)),
              end='\n\n')
    if verbose >= 2:
        print('load_data: Пример данных обучающей выборки:')
        print(x_train[5], end='\n\n')
        print('load_data: Пример метки обучающей выборки:')
        print(y_train[5], end='\n\n')
        print('load_data: Пример данных тестовой выборки:')
        print(x_test[5], end='\n\n')
        print('load_data: Пример метки обучающей выборки:')
        print(y_test[5], end='\n\n')
    if verbose >= 3:
        print('load_data: Обучающая выборка впорядке: ',
              str(len(x_train) == len(y_train)))
        print('load_data: Тестовая выборка впорядке: ',
              str(len(x_test) == len(y_test)), end='\n\n')
    return x_train, y_train, x_test, y_test


def load_dataset(train_file_name,
                 test_file_name,
                 maxlen,
                 data_converter=None,
                 marks_converter=None,
                 verbose=0):
    # Загрузка данных
    x_train, y_train, x_test, y_test = load_data(
        train_file_name,
        test_file_name,
        verbose=verbose * 3)
    # Инициализация конвертеров
    if not data_converter:
        data_converter, marks_converter = Converter.build_converters(
            x_train, x_test,
            y_train, y_test, verbose=verbose)
    # Конвертация токенов в цифровой формат
    x_train = data_converter.data_to_digital(x_train, verbose=verbose)
    y_train = marks_converter.data_to_digital(y_train, verbose=verbose)
    x_test = data_converter.data_to_digital(x_test, verbose=verbose)
    y_test = marks_converter.data_to_digital(y_test, verbose=verbose)
    # Приведение примеров к одной длине
    x_train = to_same_length(x_train, maxlen, reverse=False, verbose=verbose)
    x_test = to_same_length(x_test, maxlen, reverse=False, verbose=verbose)
    # Кодирование классов в One Hot Encoded
    y_train = vectorize_sequences(y_train, len(marks_converter), verbose=verbose)
    y_test = vectorize_sequences(y_test, len(marks_converter), verbose=verbose)

    return [x_train, y_train, x_test, y_test, data_converter, marks_converter]