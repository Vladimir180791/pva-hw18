import allure
import pytest
from pages.login_page import LoginPage

@allure.epic("Автоматизация тестирования")
@allure.feature("Демонстрация Allure отчетов")
class TestDemoAllure:
    
    @allure.story("Успешное выполнение тестов")
    @allure.title("Тест успешного выполнения с детальным логированием")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "positive")
    @allure.description("""
    ## Детальное описание теста:
    - Создание Page Object
    - Выполнение действий с логированием
    - Проверка ожидаемых результатов
    - Демонстрация работы Allure шагов
    """)
    def test_successful_demo(self):
        with allure.step("📋 Подготовка тестовых данных"):
            login_page = LoginPage()
            allure.attach("Создан объект LoginPage", "Подготовка данных", allure.attachment_type.TEXT)
        
        with allure.step("🎯 Выполнение действий на странице"):
            result = login_page.open("https://example.com/login")
            assert "Opened" in result
            
            login_result = login_page.login("test_user", "password123")
            assert "Clicked" in login_result
            
            allure.attach(f"Результат login: {login_result}", "Результат выполнения", allure.attachment_type.TEXT)
        
        with allure.step("✅ Валидация результатов"):
            assert True
            allure.attach("Все проверки пройдены успешно", "Валидация", allure.attachment_type.TEXT)
    
    @allure.story("Обработка ошибок")
    @allure.title("Тест с проверкой обработки ошибок")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "error_handling")
    @allure.description("""
    ## Тестирование обработки ошибок:
    - Получение сообщения об ошибке
    - Проверка корректности ошибки
    - Демонстрация падения теста
    """)
    def test_failed_demo(self):
        with allure.step("📋 Подготовка тестовых данных"):
            login_page = LoginPage()
        
        with allure.step("⚠️ Действие, которое приводит к ошибке"):
            error_message = login_page.get_error_message()
            allure.attach(f"Получено сообщение об ошибке: {error_message}", "Информация об ошибке", allure.attachment_type.TEXT)
        
        with allure.step("❌ Проверка, которая должна упасть"):
            # Преднамеренно неверная проверка для демонстрации
            assert "Success" in error_message, f"Ожидалось 'Success', но получено: '{error_message}'"
    
    @allure.story("Параметризованное тестирование")
    @allure.title("Параметризованный тест логина для пользователя: {username}")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("parametrized", "login")
    @pytest.mark.parametrize("username,password,expected", [
        ("user1", "pass1", True),
        ("user2", "pass2", True),
        ("invalid", "wrong", False)
    ])
    def test_parametrized_login(self, username, password, expected):
        with allure.step(f"👤 Тестирование пользователя: {username}"):
            login_page = LoginPage()
            
            with allure.step("🔑 Выполнение логина"):
                result = login_page.login(username, password)
                allure.attach(f"Результат логина: {result}", "Информация о логине", allure.attachment_type.TEXT)
            
            if expected:
                with allure.step("✅ Проверка успешного логина"):
                    assert "Clicked" in result
                    allure.attach("Логин выполнен успешно", "Успешный логин", allure.attachment_type.TEXT)
            else:
                with allure.step("❌ Проверка ошибки логина"):
                    error = login_page.get_error_message()
                    assert "Invalid" in error
                    allure.attach(f"Ошибка логина: {error}", "Ошибка авторизации", allure.attachment_type.TEXT)
    
    @allure.story("Дополнительные проверки")
    @allure.title("Тест с множественными проверками")
    @allure.severity(allure.severity_level.MINOR)
    def test_with_multiple_assertions(self):
        login_page = LoginPage()
        
        with allure.step("Проверка различных методов"):
            open_result = login_page.open("https://test.com")
            click_result = login_page.click("button")
            text_result = login_page.get_text("element")
            
            allure.attach(f"Open: {open_result}", "Результаты методов", allure.attachment_type.TEXT)
            allure.attach(f"Click: {click_result}", "Результаты методов", allure.attachment_type.TEXT)
            allure.attach(f"Text: {text_result}", "Результаты методов", allure.attachment_type.TEXT)
        
        # Все проверки должны пройти
        assert "Opened" in open_result
        assert "Clicked" in click_result
        assert "Sample" in text_result