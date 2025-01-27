from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def send_email():
    email="dioamejade@gmail.com"
    plain_text = get_template('email_template/email.txt')
    html_body = get_template('email_template/email.html')

    subject = 'Caraga HUMANS TEST'
    content = 'TEST'
    email_from = settings.EMAIL_HOST_USER

    d = {
        'message': content,
    }

    message = EmailMultiAlternatives(
        subject,
        plain_text.render(d),
        email_from,
        [email]
    )


    message.attach_alternative(html_body.render(d), 'text/html')
    message.send(fail_silently=False)