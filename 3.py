from mail import find_jetbrains_signup_link

# 输入邮箱地址和密码
email_address = 'lanoisvalkoa@hotmail.com'
password = '9V60Ck50'

# 在所有符合条件的邮件中查找链接并打印出来
signup_link = find_jetbrains_signup_link(email_address, password)
print(signup_link)
