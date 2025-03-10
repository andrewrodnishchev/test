import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class TestLogin:
    @classmethod
    def setup_class(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Запуск в безголовом режиме
        chrome_options.add_argument("--no-sandbox")  # Для CI/CD
        chrome_options.add_argument("--disable-dev-shm-usage")  # Для CI/CD

        # Используем локальный WebDriver
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @pytest.fixture(autouse=True)
    def count_tests(self):
        yield  # Запускаем тест
        # Здесь можно добавить логику для подсчета успешных и неуспешных тестов, если нужно

    def test_login(self):
        self.perform_login('rodnischev@safib.ru', '1')

        # Проверяем, что мы не перешли на страницу ClientOrg
        expected_url = 'http://lk.corp.dev.ru/ClientDevice'
        actual_url = self.driver.current_url
        assert actual_url != expected_url, "Ошибка: не удалось перейти на страницу ClientDevice."

    def perform_login(self, username, password):
        logging.info("Вводим имя пользователя")
        email_field = self.wait_for_element(By.XPATH, '//*[@id="Email"]')
        email_field.send_keys(username)

        logging.info("Вводим пароль")
        password_field = self.wait_for_element(By.CSS_SELECTOR, '#PasswordUser ')
        password_field.send_keys(password)

        logging.info("Нажимаем кнопку входа")
        login_button = self.wait_for_element(By.XPATH, '/html/body/div[1]/div/div/div/form/button')
        login_button.click()

    def wait_for_element(self, by, value):
        logging.info(f"Ожидание элемента: {by} с значением: {value}")
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, value)))
