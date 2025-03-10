import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_login():
    # Настройка драйвера (например, Chrome)
    driver = webdriver.Chrome()

    try:
        # Открываем страницу авторизации
        driver.get("http://lk.corp.dev.ru/Account/Login")  # Замените на ваш URL

        # Находим поля ввода логина и пароля и кнопку
        username_input = driver.find_element(By.NAME, "Email или Логин")  # Замените на имя поля логина
        password_input = driver.find_element(By.NAME, "Пароль")  # Замените на имя поля пароля
        login_button = driver.find_element(By.NAME, "Вход")  # Замените на имя кнопки входа

        # Вводим логин и пароль
        username_input.send_keys("rodnischev@safib.ru")  # Замените на ваш логин
        password_input.send_keys("1")  # Замените на ваш пароль

        # Нажимаем на кнопку "Вход"
        login_button.click()

        # Ждем, чтобы страница успела загрузиться
        time.sleep(5)

        # Проверка успешного входа (например, по наличию элемента на странице)
        assert "Андрей Роднищев" in driver.page_source  # Замените на текст, который появляется после входа

    finally:
        # Закрываем драйвер
        driver.quit()
