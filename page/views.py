from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from common.mailer import sendMail


def sendDemoEmail(request):
    sendMail(
        "blog@oktocode.com",
        "kayode.adechinan@gmail.com",
        "greeting",
        "<strong>Hello !</strong>",
    )
    return HttpResponse("Hello, world. You're at the polls index.")