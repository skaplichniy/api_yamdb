import random
import string
from django.core.mail import send_mail


def create_confirmation_code():
    "Создание уникального проверочного кода."
    code = str(
        random.choice(string.digits)
        + random.choice(string.ascii_uppercase)
        + random.choice(string.digits)
    )
    return code


def send_code_to_mail_of_user(email, confirmation_code, username):
    "Отправка письма с уникальным кодом новому пользователю."
    send_mail(
        subject='Регистрация на Yamdb. ',
        message=f'Здравствуйте {username}! Спасибо за регистрацию. '
                f'Код подтверждения: {confirmation_code}',
        from_email='mail-service@yambd.qwerty',
        recipient_list=[email],
    )
