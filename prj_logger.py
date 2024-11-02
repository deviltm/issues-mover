# logger_config.py

import logging

def get_logger(log_file='attachment_log.txt', log_level=logging.INFO):
    """
    Возвращает настроенный логгер, который пишет в указанный файл с заданным уровнем логирования.
    
    :param log_file: Путь к файлу для записи логов.
    :param log_level: Уровень логирования (например, logging.INFO, logging.ERROR).
    :return: Настроенный объект логгера.
    """
    logger = logging.getLogger(__name__)
    
    # Проверяем, есть ли уже обработчики для предотвращения дублирования логов
    if not logger.hasHandlers():
        logger.setLevel(log_level)
        
        # Создаем обработчик для записи логов в файл
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Формат для сообщений логгирования
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Добавляем обработчик к логгеру
        logger.addHandler(file_handler)
    
    return logger