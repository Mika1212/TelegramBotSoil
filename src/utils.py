import os
import re
import smtplib
import ssl
from email.mime.text import MIMEText

from dotenv import load_dotenv

# ЗАПОЛНИТЬ (нужна именно gmail почта и еще включенная настройка) В настройках почты ->
# Ненадежные приложения, у которых есть доступ к аккаунту -> ON
# Почта с которой идет письмо
load_dotenv()
gmail_user = "ilravgaz02@gmail.com"
gmail_password = os.getenv('GMAIL_PASSWORD')

# Почта команды
to = "soilbot30@gmail.com"


def send_mail(question, mail):
    message = question + f"\n\nПожалуйста, пришлите ответ на почту: {mail}\n\n\nПисьмо сформировано при помощи " \
                         f"телеграм-бота определения содержания углерода в почве."
    subject = "Вопрос по поводу телеграм-бота для определения содержания углерода в почве."

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(gmail_user, gmail_password)
            msg = MIMEText(message)
            msg["Subject"] = subject
            server.sendmail(gmail_user, to, f"{msg.as_string()}")
            return 0
    except:
        return -1


def message_is_mail(message):
    if re.fullmatch(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])",
            message):
        return True
    else:
        return False
