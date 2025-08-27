import allure
from .base_page import BasePage

class LoginPage(BasePage):
    # Локаторы
    USERNAME_INPUT = "username_input"
    PASSWORD_INPUT = "password_input"
    LOGIN_BUTTON = "login_button"
    ERROR_MESSAGE = "error_message"
    
    @allure.step("Выполнение входа с username: {username} и паролем: {password}")
    def login(self, username, password):
        self.logger.info(f"Attempting login with username: {username}")
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        result = self.click(self.LOGIN_BUTTON)
        return result
    
    @allure.step("Получение сообщения об ошибке")
    def get_error_message(self):
        error_text = "Invalid credentials"  # Имитация текста ошибки
        self.logger.warning(f"Error message: {error_text}")
        return error_text
    
    @allure.step("Проверка отображения ошибки")
    def is_error_displayed(self):
        self.logger.debug("Checking if error is displayed")
        return True  # Имитация отображения ошибки