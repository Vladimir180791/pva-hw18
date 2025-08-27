import allure
import logging
from utils.logger import logger

class BasePage:
    def __init__(self):
        self.logger = logger
    
    @allure.step("Открытие страницы: {url}")
    def open(self, url):
        self.logger.info(f"Opening URL: {url}")
        # В реальном проекте здесь был бы driver.get(url)
        return f"Opened {url}"
    
    @allure.step("Поиск элемента: {locator}")
    def find_element(self, locator, timeout=10):
        self.logger.debug(f"Looking for element: {locator}")
        # Имитация поиска элемента
        return f"element_{locator}"
    
    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        self.logger.info(f"Clicking on element: {locator}")
        element = self.find_element(locator)
        return f"Clicked {element}"
    
    @allure.step("Ввод текста '{text}' в элемент: {locator}")
    def type_text(self, locator, text):
        self.logger.info(f"Typing text '{text}' into element: {locator}")
        element = self.find_element(locator)
        return f"Typed '{text}' into {element}"
    
    @allure.step("Получение текста элемента: {locator}")
    def get_text(self, locator):
        self.logger.debug(f"Getting text from element: {locator}")
        # Имитация получения текста
        return "Sample text content"