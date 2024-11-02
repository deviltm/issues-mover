import requests
import os
import mimetypes
from download import yt_download_file
from prj_logger import get_logger  # Импортируем логгерl

class Attach:
    def __init__(self, youtrack_url, youtrack_token, gitea_url, gitea_token, gitea_owner, gitea_repo, download_folder):
        self.youtrack_url = youtrack_url
        self.youtrack_token = youtrack_token
        self.gitea_url = gitea_url
        self.gitea_token = gitea_token
        self.gitea_owner = gitea_owner
        self.gitea_repo = gitea_repo
        self.download_folder = download_folder
        # Устанавливаем логгер, переданный извне, или используем логгер по умолчанию
        self.logger = get_logger()

        # Создаем папку для загрузок, если она не существует
        os.makedirs(self.download_folder, exist_ok=True)

    def upload_file_to_gitea(self, file_path, issue_number):
        try:
            # URL для загрузки файла к задаче в Gitea, включая access_token в параметрах
            upload_url = f"{self.gitea_url}/api/v1/repos/{self.gitea_owner}/{self.gitea_repo}/issues/{issue_number}/assets?access_token={self.gitea_token}"
            
            # Определяем MIME тип файла автоматически
            mime_type, _ = mimetypes.guess_type(file_path)

            # Открываем файл и отправляем его в Gitea
            with open(file_path, 'rb') as f:
                response = requests.post(upload_url, headers={'accept': 'application/json'}, files={'attachment': (os.path.basename(file_path), f, mime_type)})

            if response.status_code == 201:
                self.logger.info(f"Файл '{file_path}' успешно загружен в Gitea к задаче номер {issue_number}.")
            else:
                self.logger.error(f"Ошибка при загрузке файла в Gitea: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке файла в Gitea: {e}")

    def add_attachs(self, youtrack_issue_id, gitea_issue_number):
        # Заголовки для запроса задачи в YouTrack (с авторизацией)
        youtrack_headers = {
            'Authorization': f'Bearer {self.youtrack_token}',
            'Accept': 'application/json',
        }

        # URL для получения информации о задаче с вложениями
        issue_url = f'{self.youtrack_url}/api/issues/{youtrack_issue_id}?fields=id,summary,attachments(id,name,url)'

        response = requests.get(issue_url, headers=youtrack_headers)

        # Проверка на успешный ответ и обработка вложений из задачи
        if response.status_code == 200:
            issue_data = response.json()
            self.logger.info(f"Задача ID: {issue_data['id']}")
            self.logger.info(f"Заголовок: {issue_data['summary']}")
            
            # Проверка на наличие вложений
            if 'attachments' in issue_data and issue_data['attachments']:
                self.logger.info("Вложения:")
                for attachment in issue_data['attachments']:
                    self.logger.info(f"  - Имя файла: {attachment['name']}")
                    self.logger.info(f"    URL (относительный): {attachment['url']}")
                    
                    # Скачиваем файл с полным URL
                    file_path = yt_download_file(self.youtrack_url, self.download_folder, attachment['url'], attachment['name'])
                    if file_path:  # Если файл успешно скачан
                        self.upload_file_to_gitea(file_path, gitea_issue_number)  # Загружаем файл в Gitea
            else:
                self.logger.info("Нет вложений")
        else:
            self.logger.error(f"Ошибка: {response.status_code} - {response.text}")

