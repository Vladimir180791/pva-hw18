import pytest
import allure
import logging
import os
from datetime import datetime
from utils.logger import logger

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания отчетов и прикрепления скриншотов при падении тестов
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            # Создаем директорию для скриншотов если её нет
            screenshot_dir = "allure-results/screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            # Создаем текстовый файл с информацией об ошибке (имитация скриншота)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            
            with open(screenshot_path, 'w', encoding='utf-8') as f:
                f.write(f"Test: {item.name}\n")
                f.write(f"Failed at: {datetime.now()}\n")
                f.write(f"Error: {report.longreprtext}\n")
                f.write(f"Node ID: {report.nodeid}\n")
            
            # Добавляем в allure отчет
            with open(screenshot_path, 'r', encoding='utf-8') as f:
                allure.attach(
                    f.read(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            logger.warning(f"Created error report for failed test: {item.name}")
            
        except Exception as e:
            logger.error(f"Failed to create error report: {e}")

@pytest.fixture(scope="session", autouse=True)
def configure_allure_environment():
    """
    Создание environment.properties для Allure
    """
    environment_dir = "allure-results"
    if not os.path.exists(environment_dir):
        os.makedirs(environment_dir)
    
    environment_file = os.path.join(environment_dir, "environment.properties")
    
    with open(environment_file, 'w') as f:
        f.write("PYTHON_VERSION=3.12.1\n")
        f.write("PYTEST_VERSION=7.4.3\n")
        f.write("ALLURE_VERSION=2.13.2\n")
        f.write("OS=Linux\n")
        f.write("TEST_ENV=CI\n")

@pytest.fixture(scope="function", autouse=True)
def log_test_start_end(request):
    """
    Фикстура для логирования начала и окончания каждого теста
    """
    test_name = request.node.name
    logger.info(f"🚀 Starting test: {test_name}")
    
    yield
    
    logger.info(f"✅ Finished test: {test_name}")

# Фикстура для драйвера (если будет нужна в будущем)
@pytest.fixture(scope="function")
def mock_driver():
    """
    Mock драйвер для демонстрации
    """
    class MockDriver:
        def get_screenshot_as_png(self):
            return b"mock_screenshot_data"
        
        def get(self, url):
            logger.info(f"Mock driver opening: {url}")
            return f"Mock page: {url}"
    
    return MockDriver()