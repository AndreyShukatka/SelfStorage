import os
from django.shortcuts import render
import qrcode
from django.core.mail import EmailMessage


def qrgenerator(request):
    qr_image = False
    if request.method == "POST":  # Если метод POST
        data = request.POST['data']  # Перевхатываем сообщение
        img = qrcode.make(data)
        image_path = os.path.join('media', 'qr', 'test.png')
        img.save(image_path)
        qr_image = True
        text = 'Добрый день! Ваш QR код для открывания контейнера во вложении.'  # Текст письма
        subject = 'QR код для контейнера'  # Тема письма
        to = ['slonzomby@gmail.com']  # Кому отправить
        send_email(text, subject, to, image_path)  # Отправляем сообщение с QR кодом
    return render(request, 'qrgenerator/qr.html', {'qr_image': qr_image})


def send_email(text, subject, to: list, image_path=None):
    msg = EmailMessage(
        subject=subject,
        body=text,
        to=to
    )
    msg.attach_file(image_path)
    return msg.send()
