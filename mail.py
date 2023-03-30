import poplib
import email
import re
import chardet


def find_jetbrains_signup_link(email_address, email_password):
    # 判断邮箱类型（Hotmail、Outlook 或 163 邮箱）
    if '@hotmail.' in email_address:
        pop3_server = 'pop3.live.com'
    elif '@outlook.' in email_address:
        pop3_server = 'pop-mail.outlook.com'
    elif '@163.' in email_address:
        pop3_server = 'pop.163.com'
    else:
        raise ValueError('Unsupported email provider.')

    # 连接到 POP3 服务器并登录
    server = poplib.POP3_SSL(pop3_server)
    server.user(email_address)
    server.pass_(email_password)

    # 获取邮件列表
    resp, mails, octets = server.list()

    # 遍历当前账户的所有邮件
    signup_link = None
    for i in range(1, len(mails) + 1):
        resp, lines, octets = server.retr(i)

        # 把 lines 拼接起来并解析为 Message 对象
        msg = email.message_from_bytes(b'\r\n'.join(lines))

        # 遍历 Message 对象的所有 part
        for part in msg.walk():
            # 如果 part 是 HTML 或者纯文本，那么查找其中的链接
            if part.get_content_type() in ['text/html', 'text/plain']:
                # 检测邮件内容的编码并转换为UTF-8编码
                charset = chardet.detect(part.get_payload(decode=True))['encoding']
                text = part.get_payload(decode=True).decode(charset).encode('utf-8').decode('utf-8')
                match = re.search(r'https://account.jetbrains.com/signup-complete/\S+', text)
                if match:
                    signup_link = match.group()
                    break

        if signup_link:
            break

    # 关闭当前账户的连接
    server.quit()

    return signup_link

