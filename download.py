import requests
import os

from prj_logger import get_logger  # Импортируем логгерl

def yt_download_file(youtrack_url, download_folder, relative_url, file_name):
   logger = get_logger( 'download.log')
   try:
      # Создаем полный URL для загрузки файла
      file_url = f"{youtrack_url}{relative_url}"  # Полный URL к файлу
      file_response = requests.get(file_url)  # Запрос без заголовков авторизации

      if file_response.status_code == 200:
            # Сохраняем файл
            file_path = os.path.join(download_folder, file_name)
            with open(file_path, 'wb') as f:
               f.write(file_response.content)
            logger.info(f"Файл '{file_name}' успешно скачан и сохранен в '{file_path}'")
            return file_path  # Возвращаем путь к скачанному файлу
      else:
            logger.error(f"Ошибка при скачивании файла '{file_name}': {file_response.status_code} - {file_response.text}")
            return None
   except Exception as e:
      logger.error(f"Ошибка при скачивании файла '{file_name}': {e}")
      return None