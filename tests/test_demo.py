import allure
import pytest
from pages.login_page import LoginPage

@allure.epic("Демонстрация Allure отчетов")
@allure.feature("Логирование и отчетность")
class TestDemoAllure:
    
    @pytest.fixture
    def login_page(self, driver, logger):
        """Фикстура для создания экземпляра LoginPage"""
        return LoginPage(driver, logger)
    
    @allure.story("Успешная демонстрация")
    @allure.title("Тест успешного выполнения с логированием")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Этот тест демонстрирует работу Allure отчетов с аннотациями и логированием.
    """)
    def test_successful_demo(self, login_page):
        with allure.step("Открытие страницы логина"):
            login_page.open_login_page()
        
        with allure.step("Выполнение действий на странице"):
            # Демонстрационные действия
            result = login_page.open(login_page.URL)
            
        with allure.step("Проверка результатов"):
            assert "example.com" in login_page.driver.current_url
    
    @allure.story("Демонстрация падения теста")
    @allure.title("Тест с преднамеренным падением")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_demo(self, login_page):
        with allure.step("Подготовка тестовых данных"):
            login_page.open_login_page()
        
        with allure.step("Действие, которое должно привести к ошибке"):
            # Попытка найти несуществующий элемент
            pass
            
        with allure.step("Проверка, которая упадет"):
            assert False, "Преднамеренное падение теста для демонстрации"
    
    @allure.story("Параметризованный тест")
    @allure.title("Тест с параметрами: {username}")
    @pytest.mark.parametrize("username,password,expected", [
        ("user1", "pass1", True),
        ("user2", "pass2", True),
        ("invalid", "wrong", False)
    ])
    def test_parametrized_login(self, login_page, username, password, expected):
        with allure.step(f"Тестирование пользователя: {username}"):
            login_page.open_login_page()
            
            if expected:
                # Демонстрация успешного сценария
                assert login_page.driver.title != ""
            else:
                # Демонстрация неуспешного сценария
                assert login_page.driver.current_url == login_page.URL