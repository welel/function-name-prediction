import csv


def load_data(train_file_name: str, test_file_name: str, verbose: int=0):
    '''
    Принимает на вход названия тренировочного и валидационного файлов,
    возращает 4 списка, два с метками и два с узлами.

    Returns:
        * x_train: list (тренировочные данные для обучения)
        * y_train: list (метки для валидации предсказания для тренировочной выборки)
        * x_test: list (тестовые данные для проверки модели)
        * y_test: list (метки для валидации предсказания для тестовой выборки)
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
        print('Примеров в обучающей выбоке:' + str(len(x_train)))
        print('Примеров в тестовой выбоке:' + str(len(x_test)), end='\n\n')
    if verbose >= 2:
        print('Пример данных обучающей выборки:')
        print(x_train[5])
        print('Пример метки обучающей выборки:')
        print(y_train[5], end='\n\n')
        print('Пример данных тестовой выборки:')
        print(x_test[5])
        print('Пример метки обучающей выборки:')
        print(y_test[5], end='\n\n')
    if verbose == 3:
        print('Обучающая выборка впорядке: ' + str(len(x_train) == len(y_train)))
        print('Тестовая выборка впорядке: ' + str(len(x_test) == len(y_test)), end='\n\n')
    return x_train, y_train, x_test, y_test