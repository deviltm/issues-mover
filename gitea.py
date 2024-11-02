# gitea.py
import os
import requests
from dotenv import load_dotenv
from attach import Attach  # Импортируем класс Attach
from comments import Comments  # Импортируем класс Attach
from prj_logger import get_logger  # Импортируем логгерl

class Gitea:
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
        
        # Инициализируем Attach, если включены вложения
        if self.enable_attachments:
            self.attach_handler = Attach(
                youtrack_url=self.youtrack_url,
                youtrack_token=self.youtrack_token,
                gitea_url=self.gitea_url,
                gitea_token=self.gitea_token,
                gitea_owner=self.gitea_owner,
                gitea_repo=self.gitea_repo,
                download_folder=self.download_folder
            )

        # Инициализируем Comments, если включены вложения
        if self.enable_comments:
            self.comments_handler = Comments(
                youtrack_url=self.youtrack_url,
                youtrack_token=self.youtrack_token,
                gitea_url=self.gitea_url,
                gitea_token=self.gitea_token,
                gitea_owner=self.gitea_owner,
                gitea_repo=self.gitea_repo,
                download_folder=self.download_folder
            )            
        else:
            self.comments_handler = None

        # Основные заголовки для API-запросов
        self.headers = {
            'Authorization': f'token {self.gitea_token}',
            'Content-Type': 'application/json'
        }

    def log_info(self, message):
        self.logger.info(f"[Gitea] {message}")

    def log_error(self, message):
        self.logger.error(f"[Gitea] {message}")

    def get_labels(self):
        labels = {}
        url = f'{self.gitea_url}/api/v1/repos/{self.gitea_owner}/{self.gitea_repo}/labels'
        url_org = f'{self.gitea_url}/api/v1/orgs/{self.gitea_owner}/labels'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            label_repo = {label['name']: label['id'] for label in response.json()}
            labels.update(label_repo)

            response = requests.get(url_org, headers=self.headers)
            response.raise_for_status()
            label_org = {label['name']: label['id'] for label in response.json()}
            labels.update(label_org)

            return labels
        except requests.RequestException as e:
            self.log_error(f"Ошибка при получении меток: {e}")
            return {}

    def create_labels(self, youtrack_tags):
        for label, color in youtrack_tags.items():
            label_data = {"name": label, "color": color.lstrip("#")}
            try:
                response = requests.post(
                    f'{self.gitea_url}/api/v1/repos/{self.gitea_owner}/{self.gitea_repo}/labels',
                    headers=self.headers,
                    json=label_data
                )
                response.raise_for_status()
            except requests.RequestException as e:
                self.log_error(f"Ошибка при создании метки '{label}': {e}")

    def transfer_issue(self, issue, label_id_map):
        close_label = {
            'Done': "Состояние/Готово",
            'Verified': "Состояние/Проверена",
            'Закрыта': "Состояние/Закрыта",
            'Duplicate': "Состояние/Дубликат",
            'Fixed': "Состояние/Выполнена",
            'Closed': "Состояние/Закрыта",
        }
        open_label = {
            'To Verify': "Состояние/Тестирование",
            'Open': "Состояние/Открыта",
            'In Progress': "Состояние/В работе",
            'To be discussed': "Состояние/Подлежит обсуждению",
            'Reopened': "Состояние/Открыта повторно",
            'Delayed': "Состояние/Отложена"
        }

        label_ids = [label_id_map.get(tag['name']) for tag in issue.get('tags', [])]
        label_ids = [label_id for label_id in label_ids if label_id is not None]

        closed_status = False
        assignee_names = []

        for field in issue.get('customFields', []):
            if field['projectCustomField']['field']['name'] == 'State':
                if field.get('value') and isinstance(field['value'], dict):
                    value = field['value'].get('name')
                    if (label := close_label.get(value) or open_label.get(value)):
                        label_ids.append(label_id_map.get(label))
                    if value in close_label:
                        closed_status = True
            
            if field['projectCustomField']['field']['name'] == 'Assignee':
                assignee_names = [user['login'] for user in field.get('value', []) if 'login' in user]

        issue_data = {
            "title": issue['summary'] + ' id:' + issue.get('idReadable'),
            "body": issue.get('description', ''),
            "closed": closed_status
        }
        
        if label_ids:
            issue_data["labels"] = label_ids

        if assignee_names:
            issue_data["assignees"] = assignee_names

        try:
            response = requests.post(
                f'{self.gitea_url}/api/v1/repos/{self.gitea_owner}/{self.gitea_repo}/issues',
                headers=self.headers,
                json=issue_data
            )
            response.raise_for_status()

            if response.status_code == 201:
               gitea_issue_id = response.json().get("number")
               self.log_info(f"Задача '{issue['summary']}' успешно перенесена в Gitea.")
               # Добавляем вложения, если включены
               if self.enable_attachments and self.attach_handler:
                  self.attach_handler.add_attachs(issue.get('idReadable'), gitea_issue_id)  # Вызываем метод для добавления вложений

               # Добавляем комсентарии, если включены
               if self.enable_comments and self.comments_handler:
                  self.comments_handler.add_comments(issue.get('idReadable'), gitea_issue_id)  # Вызываем метод для добавления вложений                  
 
        except requests.RequestException as e:
            self.log_error(f"Ошибка при переносе задачи: {e}")
