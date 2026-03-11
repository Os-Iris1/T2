# Настройка среды:

## Производится внутри папки, где находятся директории classifier и tele2

### Создание виртуальной среды:

#### Производится внутри папки, где находятся директории tele2, а также файлы README.md и requirements.txt

```
python -m venv .venv
```

### Запуск среды:

#### Windows

##### Командная строка Windows:

```
.venv\Scripts\activate.bat
```

##### PowerShell:

```
.venv\Scripts\Activate.ps1
```
#### Linux/MacOS с помощью bash 

```
source .venv/Scripts/activate
```

### После создания и активации среды, следует установить необходимые для проекта зависимости с помощью команды

```
pip install -r requirements.txt
```

# Настройка БД: 

Для проекта использовалась СУБД PostgreSQL. 

Настройка БД производится по пути tele2/tele2/settings.py, начиная с 82 строки, где необходимо ввести свою конфигурацию данных.
Пример конфигурации приведен ниже, а также в файле settings.py.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Tele2_Database',      # Имя базы данных
        'USER': 'postgres',             # Имя пользователя БД
        'PASSWORD': '12345678',         # Пароль пользователя
        'HOST': 'localhost',             # Хост БД (localhost для локальной разработки)
        'PORT': '5432',                   # Порт PostgreSQL (по умолчанию 5432)
    }
}
```

В папке tele2/classifier/data содержится файл churn_db.sql, из которого необходимо загрузить БД.
Для этого используется команда

```
psql -U username -d database_name < data.sql
```

Пример зарузки БД для пользователя с именем postgres и назаванием базы данных Tele2_Database:

```
psql -U postgres -d Tele2_Database < "...tele2/classifier/data/churn_db.sql"

```

Программа готова к работе после всех вышеуказанных настроек.

# Запуск серевера

Запуск сервера осуществляется в tele2/manage.py. Для этого, в терминале необходимо прописать

```
python manage.py runserver
```

После этого, локальный сервер будет доступен по адресу http://127.0.0.1:8000/

# Текущий список ресурсов локального сервера

http://127.0.0.1:8000/api/classifier/health/

http://127.0.0.1:8000/api/classifier/predict/

http://127.0.0.1:8000/api/classifier/data/

# По API:

## /api/classifier/data/ 

### GET

Получение первых 15 строк из БД.

### POST

Ожидает до двух параметров:

```
{
    "limit": 15,
    "offset": 0
}
```

Здесь limit - количество записей из БД (по умолчанию 15), а offset - смещение (по умолчанию 0)

## api/classifier/predict/

### GET 

Получение информации о состоянии модели для классификации

### POST 

Ожидает data как массив из 18 численных значений:

```
{
    "data": [10,408,0,0,0,186.1,112,31.64,190.2,66,16.17,282.8,57,12.73,11.4,6,3.08,2]
}
```

## api/classifier/health/

### GET

Получение информирует о состоянии системы
