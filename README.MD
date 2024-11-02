
# Перенос задач из YouTrack в Gitea с поддержкой вложений

Скрипт переносит задачи из YouTrack в Gitea с возможностью добавления меток, статусов и загрузки вложений.

## Требования

- **Python 3.7+**
- Модули `requests` и `python-dotenv` (устанавливаются через команду `pip install requests python-dotenv`)

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
```

2. **Запуск скрипта**:

   Скрипт можно запустить из командной строки, указав обязательные параметры. Параметры командной строки имеют приоритет над параметрами в `.env`.

   ```bash
   python main.py --youtrack_url <URL> --youtrack_token <TOKEN> --gitea_url <URL> --gitea_token <TOKEN> --gitea_owner <OWNER> --gitea_repo <REPO> --youtrack_project <PROJECT> --enable_attachments
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

## Лицензия

Этот проект доступен под лицензией MIT. См. файл `LICENSE` для подробностей
