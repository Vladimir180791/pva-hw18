import pytest
import allure
import logging
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService  # ← Правильный импорт

def is_chrome_available():
    """Проверяет, установлен ли Chrome"""
    return shutil.which("google-chrome") is not None

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Настройка логирования для всей сессии тестов"""
    from utils.logger import setup_logging
    
    log_level_name = os.getenv("PYTEST_LOG_LEVEL", "INFO")
    log_level = getattr(logging, log_level_name.upper())
    
    setup_logging(log_level=log_level)
    logging.info(f"Logging level set to: {log_level}")

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия браузера"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Пробуем разные варианты
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            logging.warning(f"Chrome failed, trying Firefox: {e}")
            # Пробуем Firefox как fallback
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(options=firefox_options)
        
        logging.info("Browser started in headless mode")
        yield driver
        
        driver.quit()
        logging.info("Browser closed")
        
    except Exception as e:
        logging.error(f"Failed to initialize any browser: {e}")
        pytest.skip(f"All browser initialization failed: {e}")

@pytest.fixture
def logger(request):
    """Фикстура для получения логгера с именем теста"""
    test_name = request.node.name
    return logging.getLogger(test_name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            driver = item.funcargs.get('driver')
            if driver:
                # Создаем директорию для скриншотов если её нет
                screenshot_dir = "screenshots"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                # Сохраняем скриншот
                screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
                driver.save_screenshot(screenshot_path)
                
                # Добавляем в allure отчет
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logging.warning(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logging.error(f"Failed to take screenshot: {e}")
