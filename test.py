import logging
import time
from unittest.mock import patch

import pytest
import requests
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Инициализация colorama
init(autoreset=True)
logging.basicConfig(level=logging.DEBUG)

class TestLogin:
    total_tests = 0
    success_tests = 0
    failed_tests = 0
    telegram_bot_token = '7414360296:AAGisDw14CHmiaibMvkF1XsRvYreXKDXHNI'  # Замените на ваш токен
    chat_id = '950609832'  # Замените на ваш chat_id

    @classmethod
    def setup_class(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--headless")  # Запуск в безголовом режиме
        chrome_options.add_argument("--no-sandbox")  # Для CI/CD окружений
        chrome_options.add_argument("--disable-dev-shm-usage")  # Для CI/CD окружений
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @pytest.fixture(autouse=True)
    def count_tests(self):
        TestLogin.total_tests += 1
        test_successful = True

        try:
            yield
        except Exception as e:
            TestLogin.failed_tests += 1
            test_successful = False
            print(Fore.RED + f"Ошибка: {str(e)}")
            raise
        finally:
            if test_successful:
                TestLogin.success_tests += 1

    @patch('requests.post')  # Мокируем requests.post
    def test_login(self, mock_post):
        # Настройка мокированного ответа
        mock_post.return_value = self.mock_response(200)

        self.perform_login('rodnischev@safib.ru', '1')  # Используем неправильный пароль

        # Проверяем, что мы не перешли на страницу ClientOrg
        expected_url = 'http://lk.corp.dev.ru/ClientDevice'
        actual_url = self.driver.current_url
        assert actual_url != expected_url, Fore.RED + "Ошибка: не удалось перейти на страницу ClientDevice."

    def perform_login(self, username, password):
        self.wait_for_element(By.XPATH, '//*[@id="Email"]').send_keys(username)
        self.wait_for_element(By.CSS_SELECTOR, '#PasswordUser ').send_keys(password)
        self.wait_for_element(By.XPATH, '/html/body/div[1]/div/div/div/form/button').click()
        time.sleep(3)  # Задержка после нажатия кнопки логина

    def wait_for_element(self, by, value):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, value)))

    def mock_response(self, status_code):
        mock_response = requests.Response()
        mock_response.status_code = status_code
        return mock_response

    def send_telegram_message(self, message):
        url = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage'
        payload = {'chat_id': self.chat_id, 'text': message}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Проверка на ошибки HTTP
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Ошибка отправки сообщения в Telegram: {e}")
