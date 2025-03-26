from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import smtplib

def send_email(email,notify_type,activity):
    email="dioamejade@gmail.com"
    plain_text = get_template('email_template/email.txt')
    html_body = get_template('email_template/email.html')

    subject = 'Caraga HUMANS TEST'
    content = notify_type + ' ' + activity
    email_from = 'DSWD Field Office Caraga <dswd.focrg@dswd.gov.ph>'

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


# def send_email():
#     # Connect to MailHog on port 1025 without STARTTLS
#     server = smtplib.SMTP('localhost', 1025)

#     # Login (if necessary, but MailHog usually doesn't require it)
#     # server.login('your_username', 'your_password')

#     # Send the email
#     server.sendmail('from@example.com', 'dioamejade@gmail.com', 'Subject: Test\n\nThis is a test email.')
#     server.quit()