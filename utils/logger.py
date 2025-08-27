import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Создаем форматтер
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Создаем консольный обработчик
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        
        # Создаем файловый обработчик
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        
        # Добавляем обработчики к логгеру
        if not self.logger.handlers:
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
    
    def get_logger(self):
        return self.logger

# Создаем экземпляр логгера для использования в проекте
logger = Logger(__name__).get_logger()