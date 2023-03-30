import time
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from mail import find_jetbrains_signup_link
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_email_prefix(email_address):
    return email_address.split('@')[0]

def generate_password(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_account(email_address, email_password):
    first_name = generate_random_string(5)
    last_name = generate_random_string(5)
    email_prefix = generate_email_prefix(email_address)
    account_password = generate_password(10)
    return (first_name, last_name, email_prefix, account_password)


# 从 mail.txt 文件中读取邮箱账号和密码
with open('mail.txt') as f:
    accounts = [line.strip().split('----') for line in f.readlines()]

# 循环注册账户并保存账户信息到 accounts.txt 文件中
for email_address, email_password in accounts:
    # 打开 Chrome 浏览器实例
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.set_window_size(590, 900)
    driver.delete_all_cookies()
    # 打开登录页面
    driver.get('https://account.jetbrains.com/login')

    # 输入邮箱
    email_input = driver.find_element(By.XPATH, '//*[@id="email"]')
    email_input.send_keys(email_address)

    # 点击注册按钮
    register_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/form/div[2]/button')
    register_button.click()

    # 等待页面加载完成并出现 'we just emailed to you' 文字
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*'), 'we just emailed to you'))
    print(f'{email_address} 注册邮件发送成功')

    time.sleep(20)

    # 在所有符合条件的邮件中查找链接并打印出来
    signup_link = find_jetbrains_signup_link(email_address, email_password)
    print(f'{email_address} 注册链接：{signup_link}')

    # 在当前页面中打开注册链接
    driver.get(signup_link)
    print(f'{email_address} 注册链接打开成功')

    # 随机生成用户名
    username = email_address.split('@')[0] + '_' + ''.join(random.choices(string.digits, k=3))

    # 随机生成密码
    password_length = 10
    chars = string.ascii_letters + string.digits
    account_password = ''.join(random.choices(chars, k=password_length))

    # 随机生成名和姓
    first_name = ''.join(random.choices(string.ascii_uppercase, k=3))
    last_name = ''.join(random.choices(string.ascii_uppercase, k=5))

    # 随机生成用户名和密码，并填写注册信息
    first_name_input = driver.find_element(By.XPATH, '//*[@id="firstName"]')
    first_name_input.send_keys(first_name)

    last_name_input = driver.find_element(By.XPATH, '//*[@id="lastName"]')
    last_name_input.send_keys(last_name)

    email_prefix_input = driver.find_element(By.XPATH, '//*[@id="userName"]')
    email_prefix_input.send_keys(username)

    password_input = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys(account_password)

    password_confirm_input = driver.find_element(By.XPATH, '//*[@id="pass2"]')
    password_confirm_input.send_keys(account_password)

    agree_checkbox = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/form/div[1]/div[1]/div/div[8]/div[2]/div/label/input')
    agree_checkbox.click()

    privacy_checkbox = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/form/div[2]/div/div/div/div/div/div/ul/li/div/label/input')
    privacy_checkbox.click()

    submit_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/form/div[3]/div/div/div[2]/button')
    submit_button.click()

    # 等待页面加载完成并出现 'No Available Licenses' 文字
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*'), 'No Available Licenses'))
    print(f'{email_address} 注册成功')

    # 关闭当前账户的浏览器实例
    driver.quit()

    # 保存账户信息到 accounts.txt 文件中
    with open('accounts.txt', 'a') as f:
        f.write(f'{email_address}----{email_password}----{username}----{account_password}\n')

