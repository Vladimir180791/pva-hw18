import allure
import pytest
from pages.login_page import LoginPage

@allure.epic("Авторизация")
@allure.feature("Функциональность входа в систему")
class TestLogin:
    
    @allure.story("Успешный вход в систему")
    @allure.title("Тест успешной авторизации с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Этот тест проверяет успешный вход в систему с корректными учетными данными.
    Ожидается переход на главную страницу после авторизации.
    """)
    def test_successful_login(self, driver):
        with allure.step("Открытие страницы логина"):
            login_page = LoginPage(driver)
            login_page.open("https://example.com/login")
        
        with allure.step("Ввод корректных учетных данных"):
            login_page.login("valid_user", "valid_password")
        
        with allure.step("Проверка успешной авторизации"):
            assert "dashboard" in driver.current_url
            assert "Welcome" in driver.page_source
    
    @allure.story("Неуспешный вход в систему")
    @allure.title("Тест авторизации с неверными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_login(self, driver):
        with allure.step("Открытие страницы логина"):
            login_page = LoginPage(driver)
            login_page.open("https://example.com/login")
        
        with allure.step("Ввод неверных учетных данных"):
            login_page.login("invalid_user", "wrong_password")
        
        with allure.step("Проверка отображения ошибки"):
            assert login_page.is_error_displayed()
            error_text = login_page.get_error_message()
            assert "Invalid credentials" in error_text