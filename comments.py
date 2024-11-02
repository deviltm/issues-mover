import os
import requests
import json
from datetime import datetime
from download import yt_download_file
from prj_logger import get_logger  # Импортируем логгерl

class Comments:
    def __init__(self, youtrack_url, youtrack_token, gitea_url, gitea_token, gitea_owner, gitea_repo, download_folder):
        """
        Инициализация класса с настройками для подключения к YouTrack и Gitea.

        :param youtrack_url: URL для YouTrack API.
        :param youtrack_token: Токен для авторизации в YouTrack.
        :param gitea_url: URL для Gitea API.
        :param gitea_token: Токен для авторизации в Gitea.
        :param gitea_owner: Владелец репозитория Gitea.
        :param gitea_repo: Название репозитория Gitea.
        :param download_folder: Папка для сохранения вложений.
        """
        self.youtrack_url = youtrack_url
        self.youtrack_token = youtrack_token
        self.gitea_url = gitea_url
        self.gitea_token = gitea_token
        self.gitea_owner = gitea_owner
        self.gitea_repo = gitea_repo
        self.download_folder = download_folder
        os.makedirs(download_folder, exist_ok=True)

        # Устанавливаем логгер, переданный извне, или используем логгер по умолчанию
        self.logger = get_logger()

    def get_comments(self, issue_id):
        """
        Получает комментарии из задачи YouTrack и скачивает вложения.

        :param issue_id: Идентификатор задачи в YouTrack.
        :return: Список комментариев с вложениями.
        """
        headers = {
            'Authorization': f'Bearer {self.youtrack_token}',
            'Accept': 'application/json',
        }
        comments_url = f'{self.youtrack_url}/api/issues/{issue_id}/comments?fields=id,text,created,author(login,fullName),attachments(id,name,url)'
        response = requests.get(comments_url, headers=headers)

        if response.status_code == 200:
            comments = response.json()
            for comment in comments:
                if 'attachments' in comment and comment['attachments']:
                    for attachment in comment['attachments']:
                        yt_download_file(self.youtrack_url, self.download_folder, attachment['url'], attachment['name'])
            return comments
        else:
            self.logger.error(f"Ошибка получения комментариев: {response.status_code} - {response.text}")
            return None

    def post_comment_to_gitea(self, issue_number, comment_text, attachments=[]):
        """
        Создает комментарий в Gitea и прикрепляет вложения.

        :param issue_number: Номер задачи в Gitea.
        :param comment_text: Текст комментария.
        :param attachments: Список путей к файлам для вложения.
        """
        headers = {
            'Accept': 'application/json'
            'Content-Type: application/json'
        }
        comment_url = f"{self.gitea_url}/api/v1/repos/{self.gitea_owner}/{self.gitea_repo}/issues/{issue_number}/comments?access_token={self.gitea_token}"
        data = {"body": comment_text }
        response = requests.post(comment_url, headers=headers, json=data)

        if response.status_code == 201:
            self.logger.info(f"Комментарий добавлен в Gitea: {comment_text}")
            commit_id = response.json().get("id")
            for file_path in attachments:
                self.upload_attachment_to_gitea(commit_id, file_path)
        else:
            self.logger.error(f"Ошибка при добавлении комментария: {response.status_code} - {response.text}")

    def upload_attachment_to_gitea(self, issue_number, file_path):
        """
        Загружает вложение в комментарий Gitea.

        :param issue_number: Номер задачи в Gitea.
        :param file_path: Путь к файлу для загрузки.
        """
        headers = {
            'Authorization': f'token {self.gitea_token}',
        }
        attachment_url = f"{self.gitea_url}/api/v1/repos/{self.gitea_owner}/{self.gitea_repo}/issues/comments/{issue_number}/assets"

        with open(file_path, 'rb') as file:
            files = {'attachment': file}
            response = requests.post(attachment_url, headers=headers, files=files)

        if response.status_code == 201:
            self.logger.info(f"Вложение '{file_path}' загружено в Gitea")
            os.remove(file_path)

        else:
            self.logger.error(f"Ошибка при загрузке вложения: {response.status_code} - {response.text}")

    def add_comments(self, youtrack_issue_id, gitea_issue_number):
        """
        Обрабатывает задачу: получает комментарии из YouTrack и добавляет их в Gitea.

        :param youtrack_issue_id: Идентификатор задачи в YouTrack.
        :param gitea_issue_number: Номер задачи в Gitea.
        """
        comments = self.get_comments(youtrack_issue_id)
        if comments:
            for comment in comments:
                comment_text = comment['text']
                fullName = comment['author'].get('fullName')
                login = comment['author'].get('login')
                comment_text = "[" + fullName+ "]("+self.gitea_url+"/"+login+")\n" + comment['text']
                attachments = [os.path.join(self.download_folder, att['name']) for att in comment.get('attachments', [])]
                self.post_comment_to_gitea(gitea_issue_number, comment_text, attachments)

