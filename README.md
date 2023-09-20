# Сервис YaCut

## Описание проекта

Сервис YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать 
длинную пользовательскую ссылку с короткой, которую предлагает сам 
пользователь или предоставляет сервис.

Ключевые возможности сервиса:
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам.

## Стек технологий:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/-Flask-464646?logo=flask)](https://palletsprojects.com/p/flask/)
[![Flask-SQLAlchemy](https://img.shields.io/badge/-FlaskSQLAlchemy-464646?logo=flask)](https://flask-sqlalchemy.palletsprojects.com/en/latest/)
[![Jinja](https://img.shields.io/badge/-Jinja-464646?logo=Jinja)](https://palletsprojects.com/p/jinja/)
[![Flask-WTF](https://img.shields.io/badge/-FlaskWTF-464646?logo=Flask)](https://flask-wtf.readthedocs.io/en/latest/)
[![Flask-Migrate](https://img.shields.io/badge/-Flask_Migrate-464646?logo=Flask)](https://flask-migrate.readthedocs.io/en/latest/index.html)
## API для проекта

API проекта доступен всем желающим. Сервис обслуживает только два эндпоинта:
* /api/id/ — POST-запрос на создание новой короткой ссылки;
* /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.

## Установка и запуск:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Автор: [Титов Максим](https://github.com/Maximuz2004)