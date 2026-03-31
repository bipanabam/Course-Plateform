from django.shortcuts import render
from django.db import transaction

from emails.forms import EmailForm
from emails.models import Email, EmailVerificationEvent

from emails import services

def homepage(request, *args, **kwargs):
    template_name = "home.html"
    print(f'path: {request.path}')
    return render(request, template_name)