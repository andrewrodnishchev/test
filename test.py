from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_login():
    options = Options()
    options.add_argument("--ignore-certificate-errors")  # Игнорировать ошибки SSL
    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        driver.get("http://lk.corp.dev.ru/Account/Login")  # Замените на ваш URL

        # Явное ожидание появления поля ввода логина
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/form/div[1]/input'))  # XPath для поля логина
        )

        # Явное ожидание появления поля ввода пароля
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/form/div[2]/input'))  # XPath для поля пароля
        )

        # Явное ожидание появления кнопки входа
        login_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/form/button'))  # XPath для кнопки
        )

        # Вводим логин и пароль
        username_input.send_keys("rodnischev@safib.ru")  # Замените на ваш логин
        password_input.send_keys("1")  # Замените на ваш пароль

        # Нажимаем кнопку входа
        login_button.click()

    finally:
        driver.quit()

# Запуск теста
test_login()
