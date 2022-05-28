import os
import smtplib

from configparser import ConfigParser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

def extract_tests(file):
    """Извлекает тесты из файла."""
    tests = []
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()

        # Убираем \n и формируем список типа [вопрос, ответ]
        st = 1
        for i in data:
            if st == 1:
                i = i.replace("\n", "");
                q = []
                q.append(i)
                st = 2
            else:
                i = i.replace("\n", "");
                q.append(i)
                tests.append(q)
                st = 1
    return tests

def create_generator(lists):
    for i in lists:
        yield i

def save_log(lst_log, test_name, us_name, us_mail,number_questions, value_crct, value_incrct):
    """Сохраняет вопросы,ответы пользователя,правильные ответы, данные счетчиков в файл txt."""

    try:
        prc = (value_crct/ number_questions) * 100
    except ZeroDivisionError:
        prc = 0

    path = f'{test_name}_test.txt'
    with open(path, 'w',encoding='utf-8') as file:
        file.write(f'\t\t\t{test_name.upper()} TEST')
        file.write('\n\n')
        file.write(f'Имя: {us_name} \n')
        file.write(f'E-mail: {us_mail} \n')
        file.write(str(f'Всего вопросов: {number_questions} \n'))
        file.write(str(f'Правильных ответов: {value_crct} \n'))
        file.write(str(f'Неправильных ответов: {value_incrct} \n'))
        file.write(str(f'Выполнено правильно: {prc} % \n'))
        file.write('\n')
        i = 1
        for log in lst_log:
            file.write(str(f'{i}) Вопрос: {log[0]} \n'))
            file.write(f'Ваш ответ: {log[2]} \n')
            file.write(f'Правильный ответ: {log[1]} \n')
            file.write('########################\n')
            i += 1
    return path


def send_mail(to_addr, name, file_to_attach,):
    """Отправка фaйла txt на email."""

    flag = ''
    encode = 'utf-8'
    # Проверка файла с данными авторизации .
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")

    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        flag = "Ошибка. Отсутствует файл конфигурации 'email.ini'."
        return flag
    # Получение данных авторизации из файла.
    server = cfg.get("smtp", "server")
    port = cfg.get("smtp", "port")
    from_addr = cfg.get("smtp", "email")
    passwd = cfg.get("smtp", "passwd")

    subject = f'Прохождение теста {name}.'
    text = f'Ваши ответы на тест {name}.'

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg['Text'] = text
    msg["Date"] = formatdate(localtime=True)
    msg["To"] = to_addr

    attachment = MIMEBase('application', "octet-stream")
    header = 'Content-Disposition', f'attachment; filename="{file_to_attach}"'

    # Переобразование вложения в бинарный код
    try:
        with open(file_to_attach, "rb") as fh:
            data = fh.read()
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        flag = f"Ошибка при открытии файла вложения {file_to_attach}"
        return flag

    # Отправка сообщения.
    flag = 'Отправлено!'
    try:
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_addr, passwd)
        smtp.sendmail(from_addr, to_addr, msg.as_string())
    except smtplib.SMTPException:
        flag = "Ошибка. Не верная конфигурация 'email.ini'."
    finally:
        smtp.quit()

    return flag
