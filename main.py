import os
import argparse
from dotenv import load_dotenv
from youtrack import YouTrack
from gitea import Gitea
from prj_logger import get_logger  # Импортируем логгерl

def main():
    logger = get_logger( 'log.txt')

    load_dotenv()

    parser = argparse.ArgumentParser(description="Перенос задач из YouTrack в Gitea с поддержкой вложений.")

    parser.add_argument('--youtrack_url', type=str,
                        help='URL YouTrack, например, https://youtrack.example.com')
    parser.add_argument('--youtrack_token', type=str,
                        help='API токен для доступа к YouTrack.')
    parser.add_argument('--gitea_url', type=str,
                        help='URL Gitea, например, https://gitea.example.com')
    parser.add_argument('--gitea_token', type=str,
                        help='API токен для доступа к Gitea.')
    parser.add_argument('--gitea_owner', type=str,
                        help='Имя владельца репозитория в Gitea.')
    parser.add_argument('--gitea_repo', type=str,
                        help='Название репозитория в Gitea для импорта задач.')
    parser.add_argument('--youtrack_project', type=str,
                        help='Имя проекта в YouTrack, из которого будут импортированы задачи.')
    parser.add_argument('--download_folder', type=str, default='./downloads',
                        help='Папка для загрузки вложений из YouTrack (по умолчанию ./downloads).')
    parser.add_argument('--enable_attachments', action='store_true',
                        help='Включить загрузку и перенос вложений задач (по умолчанию выключено).')
    parser.add_argument('--enable_comments', action='store_true',
                        help='Включить загрузку и перенос комментариев с вложениями к задаче (по умолчанию выключено).')

    args = parser.parse_args()

    settings = {
        'youtrack_url': args.youtrack_url or os.getenv('YOUTRACK_URL'),
        'youtrack_token': args.youtrack_token or os.getenv('YOUTRACK_TOKEN'),
        'gitea_url': args.gitea_url or os.getenv('GITEA_URL'),
        'gitea_token': args.gitea_token or os.getenv('GITEA_TOKEN'),
        'gitea_owner': args.gitea_owner or os.getenv('GITEA_OWNER'),
        'gitea_repo': args.gitea_repo or os.getenv('GITEA_REPO'),
        'youtrack_project': args.youtrack_project or os.getenv('YOUTRACK_PROJECT'),
        'download_folder': args.download_folder or os.getenv('DOWNLOAD_FOLDER', './downloads'),
        'enable_attachments': args.enable_attachments or (os.getenv('ENABLE_ATTACHMENTS', 'false').lower() == 'true'),
        'enable_comments': args.enable_attachments or (os.getenv('ENABLE_COMMENTS', 'false').lower() == 'true')
    }

    required_params = ['youtrack_url', 'youtrack_token', 'gitea_url', 'gitea_token', 'gitea_owner', 'gitea_repo', 'youtrack_project']
    missing_params = [param for param in required_params if not settings[param]]
    if missing_params:
        parser.print_help()
        raise ValueError(f"Ошибка: Необходимо указать следующие обязательные параметры: {', '.join(missing_params)}")

    gitea = Gitea(settings)
    youtrack = YouTrack(settings)

    issues = youtrack.fetch_issues(settings['youtrack_project'])
    label_map = gitea.get_labels()

    # Проверка, что label_map не None и не пустой
    if label_map:

        youtrack_tags = {
            tag['name']: tag['color'].get('background') for issue in issues for tag in issue.get('tags', [])
        }

        # Фильтрация и создание меток, которые отсутствуют в label_map
        new_labels = {tag: background for tag, background in youtrack_tags.items() if tag not in label_map}
        
        if new_labels:
            gitea.create_labels(new_labels)
            label_map = gitea.get_labels()
        else:
            logger.info("Новые метки отсутствуют для создания.")
    else:
        logger.error("Ошибка: не удалось получить существующие метки.")


    # Сортируем задачи по номеру в проекте
    issues_sorted = sorted(issues, key=lambda x: x['numberInProject'])


    for issue in issues_sorted:
        gitea.transfer_issue(issue, label_map)

if __name__ == "__main__":
   main()
