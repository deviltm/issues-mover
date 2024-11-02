# Перенос задач из YouTrack в Gitea с поддержкой вложений

Скрипт для переноса задач из YouTrack в Gitea с возможностью добавления меток, статусов и загрузки вложений.

## Требования

- **Python 3.7+**
- Модули `requests` и `python-dotenv` (установка: `pip install requests python-dotenv`)

## Настройка

1. **Создайте файл `.env`** в корне проекта и укажите следующие параметры:

```env
YOUTRACK_URL=https://youtrack.example.com
YOUTRACK_TOKEN=ваш_токен_YouTrack
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=ваш_токен_Gitea
GITEA_OWNER=владелец_репозитория
GITEA_REPO=название_репозитория
YOUTRACK_PROJECT=имя_проекта_YouTrack
DOWNLOAD_FOLDER=./downloads
ENABLE_ATTACHMENTS=true
ENABLE_COMMENTS=true
```

2. **Запуск скрипта**:

    Запустите скрипт из командной строки, указав обязательные параметры. Параметры командной строки имеют приоритет над параметрами в `.env`.

```bash
python main.py --youtrack_url <URL> --youtrack_token <TOKEN> --gitea_url <URL> --gitea_token <TOKEN> --gitea_owner <OWNER> --gitea_repo <REPO> --youtrack_project <PROJECT> --enable_attachments --enable_comments
```

    для разных проектов можно записать основные настройки в .env а часть менять ключами при запуске, ключи имеют приоритет.

```bash
python main.py --enable_attachments --enable_comments
```

**Параметры:**

- `--youtrack_url`: URL для доступа к YouTrack
- `--youtrack_token`: API-токен для YouTrack
- `--gitea_url`: URL для доступа к Gitea
- `--gitea_token`: API-токен для Gitea
- `--gitea_owner`: Имя владельца репозитория
- `--gitea_repo`: Название репозитория
- `--youtrack_project`: Имя проекта в YouTrack
- `--download_folder`: Путь для сохранения вложений (по умолчанию `./downloads`)
- `--enable_attachments`: Флаг для загрузки вложений в Gitea (по умолчанию выключен)

## Особенности

- Переносит метки и статусы задач из YouTrack в Gitea.
- Загружает вложения, если активирован флаг `--enable_attachments`.
- Загружает комментарии к задачам с вложениями, если активирован флаг `--enable_comments`.
- Автоматически закрывает задачи в Gitea при создании, основываясь на статусах из YouTrack. В настоящее время статусы прописаны вручную в `gitea.py` на 99 и 107 строках как `close_label` и `open_label`. Метки в YouTrack определяют статус и соответствующую метку в Gitea для задачи. Эти метки должны быть предварительно созданы в Gitea. Пример меток см. в `labels.yaml`.
- Новые задачи автоматически назначаются исполнителям из YouTrack. Проверка наличия исполнителя в Gitea пока не реализована, что может вызвать ошибки при добавлении задачи.
- В случае ошибки задачи пропускаются.
- Автоматически ведется журнал (`log.txt`) для `info` и `error`.
- Проверено на 2000 и 1500 задачах.
- На время переноса рекомендуется отключить все хуки и уведомления, чтобы избежать спама.
- Задачи добавляются от пользователя, чей токен используется; требуются максимальные права.
- Установить создателя и дату создания задач через API невозможно. Для этого потребуется переписать логику добавления задач напрямую через базу данных.

## Лицензия

Проект доступен по лицензии MIT. Подробности см. в файле `LICENSE`.
