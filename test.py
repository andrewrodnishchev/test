import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot
import asyncio
import tempfile

class TestLogin:
    total_tests = 0
    success_tests = 0
    failed_tests = 0

    @classmethod
    def setup_class(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=' + tempfile.mkdtemp())  # Уникальная директория для пользовательских данных
        options.add_argument('--headless')  # Опционально, если не нужен GUI
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        cls.print_final_results()
        asyncio.run(cls.send_notification())  # Отправка уведомления после завершения тестов

    @classmethod
    def print_final_results(cls):
        print(f"\nИтоговые результаты:")
        print(f"Успешные тесты: {cls.success_tests}")
        print(f"Неуспешные тесты: {cls.failed_tests}")

    @classmethod
    async def send_notification(cls):
        bot = Bot(token='7414360296:AAGisDw14CHmiaibMvkF1XsRvYreXKDXHNI')
        chat_id = '950609832'
        message = f"🎉 Итоги автотестов:\nУспешные тесты: {cls.success_tests}\nНеуспешные тесты: {cls.failed_tests}"
        await bot.send_message(chat_id=chat_id, text=message)

    @pytest.fixture(autouse=True)
    def count_tests(self):
        TestLogin.total_tests += 1
        try:
            yield
        except Exception:
            TestLogin.failed_tests += 1
            raise
        else:
            TestLogin.success_tests += 1

    def test_login(self):
        driver = self.driver
        driver.get('http://lk.pub.dev.ru/Account/Login')

        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Email"]'))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#PasswordUser '))
        )

        username_input.send_keys('ast10@mailforspam.com')
        password_input.send_keys('1')

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/form/button'))
        )
        login_button.click()

        print("Вход выполнен успешно!")

if __name__ == "__main__":
    pytest.main(["-q", "--disable-warnings"])
