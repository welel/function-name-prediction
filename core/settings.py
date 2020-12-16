import os



DATASETS_FOLDER = 'datasets/'

# Путь к архиву с исходным датасетом
ARCHIVE_PATH = os.path.join(DATASETS_FOLDER, 'py150.tar.gz')

# Пути к разархивированным датасетам
DATASET_TRAIN_PATH = os.path.join(DATASETS_FOLDER, 'python100k_train.json')
DATASET_EVAL_PATH = os.path.join(DATASETS_FOLDER, 'python50k_eval.json')

# Путь к извлеченным функциям из датасетов
FUNCTIONS_PATH = os.path.join(DATASETS_FOLDER, 'functions.json')

# Путь к отфильтрованным функциям
FILTERED_FUNCTIONS_PATH = os.path.join(DATASETS_FOLDER, 'filtered_functions.json')

# Путь к финальному, готовому датасету
DATASET_PATH = os.path.join(DATASETS_FOLDER, 'dataset.csv')

# Путь к json файлам, хранящим словари-счетчики уникальных значений
UNIQ_NAMES_PATH = os.path.join(DATASETS_FOLDER, 'uniq_names.json')
UNIQ_VALUES_PATH = os.path.join(DATASETS_FOLDER, 'uniq_values.json')
