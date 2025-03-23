from django.shortcuts import render
from django.db import transaction

from emails.forms import EmailForm
from emails.models import Email, EmailVerificationEvent

from emails import services

def homepage(request, *args, **kwargs):
    template_name = "home.html"
    form = EmailForm(request.POST or None)
    context = {
        'form': form,
        'message': ""
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        services.start_verification_event(email)
        context['form'] = EmailForm()
        context['message'] = "Success! Check your email for verification."
    else:
        print(form.errors)

    # print(f"Email: {request.session['email_id']}")
    return render(request, template_name, context)