# youtrack.py
import os
import requests
from dotenv import load_dotenv
from prj_logger import get_logger  # Импортируем логгерl

class YouTrack:
    def __init__(self, settings):
        self.youtrack_url = settings['youtrack_url']
        self.youtrack_token = settings['youtrack_token']
        self.gitea_url = settings['gitea_url']
        self.gitea_token = settings['gitea_token']
        self.gitea_owner = settings['gitea_owner']
        self.gitea_repo = settings['gitea_repo']
        self.download_folder = settings['download_folder']
        self.enable_attachments = settings['enable_attachments']
        self.enable_comments = settings['enable_comments']
        # Устанавливаем логгер, переданный извне, или используем логгер по умолчанию
        self.logger = get_logger()

        # Основные заголовки для API-запросов
        self.headers = {
            'Authorization': f'Bearer {self.youtrack_token}',
            'Content-Type': 'application/json'
        }

    def log_error(self, message):
        print(f"[YouTrack] {message}")

    def log_info(self, message):
        print(f"[YouTrack] {message}")

    def get_total_issue_count(self, project_name):
        total_count = 0
        page_size = 450
        url = f'{self.youtrack_url}/api/issues'
        
        try:
            while True:
                params = {
                    'fields': 'idReadable',
                    'query': f'project: {project_name}',
                    '$top': page_size,
                    '$skip': total_count
                }

                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                issues = response.json()

                if not issues:
                    break

                total_count += len(issues)

        except requests.RequestException as e:
            self.log_error(f"Ошибка при получении общего количества задач: {e}")
            if 'response' in locals():
                self.log_error(f"Ответ сервера: {response.text}")

        return total_count

    def fetch_issues(self, project_name):
        issues = []
        total_count = self.get_total_issue_count(project_name)
        batch_size = 450

        for offset in range(0, total_count, batch_size):
            url = f'{self.youtrack_url}/api/issues'
            params = {
                'fields': 'idReadable,summary,description,project,numberInProject,linkedIssues,customFields(projectCustomField(name,field(name)),value(name,login)),tags(name,color(background, foreground))',
                'query': f'project: {project_name}',
                '$top': batch_size,
                '$skip': offset
            }

            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                batch_issues = response.json()
                issues.extend(batch_issues)

            except requests.RequestException as e:
                self.log_error(f"Ошибка при получении задач: {e}")

        return issues

    def fetch_issue_comments(self, issue_id):
        url = f'{self.youtrack_url}/api/issues/{issue_id}/timeTracking/workItems'
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.log_error(f"Ошибка при получении комментариев для задачи {issue_id}: {e}")
            return []
