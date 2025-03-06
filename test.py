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
        options.add_argument('--user-data-dir=' + tempfile.mkdtemp())
        options.add_argument('--headless')  # Запуск в фоновом режиме
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        cls.print_final_results()
        asyncio.run(cls.send_notification())

    @classmethod
    def print_final_results(cls):
        print(f"\nИтоговые результаты:")
        print(f"Успешные тесты: {cls.success_tests}")
        print(f"Неуспешные тесты: {cls.failed_tests}")

    @classmethod
    async def send_notification(cls):
        bot = Bot(token='YOUR_BOT_TOKEN')  # Замените на ваш токен
        chat_id = 'YOUR_CHAT_ID'  # Замените на ваш chat_id
        message = f"🎉 Итоги автотестов:\nУспешные тесты: {cls.success_tests}\nНеуспешные тесты: {cls.failed_tests}"
        await bot.send_message(chat_id=chat_id, text=message)

    @pytest.fixture(autouse=True)
    def count_tests(self):
        TestLogin.total_tests += 1
        try:
            yield
        except Exception:
            TestLogin.failed_tests += 1  # Увеличиваем счетчик неуспешных тестов
            raise  # Пробрасываем исключение дальше
        else:
            TestLogin.success_tests += 1  # Увеличиваем счетчик успешных тестов, если исключение не возникло

    def test_login(self):
        driver = self.driver
        driver.get('http://lk.corp.dev.ru')

        # Вводим неправильные учетные данные
        username_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="Email"]'))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#PasswordUser  '))
        )

        username_input.send_keys('ast10@mailforspam.com')  # Ваш email
        password_input.send_keys('НеправильныйПароль')  # Неправильный пароль

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/form/button'))
        )
        login_button.click()

        # Проверка на наличие сообщения об ошибке
        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Неудачная попытка аутентификации. Ошибка Active Directory: Не определен домен Active Directory")]'))
            )
            assert error_message is not None, "Ошибка входа не обнаружена, тест завершился неуспешно!"
            print("Ошибка входа обнаружена, тест завершен успешно!")
        except Exception as e:
            print(f"Тест завершился неуспешно: {e}")
            raise  # Пробрасываем исключение, чтобы счетчик неуспешных тестов увеличился

if __name__ == "__main__":
    pytest.main(["-q", "--disable-warnings"])
