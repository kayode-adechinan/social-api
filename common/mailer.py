from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


# blog@oktocode.com
def sendMail(sender, to, subject, body):
    text_content = strip_tags(body)
    html_content = body
    msg = EmailMultiAlternatives(subject, text_content, sender, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

