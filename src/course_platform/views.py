from django.shortcuts import render
from django.db import transaction

from emails.forms import EmailForm
from emails.models import Email, EmailVerificationEvent

def homepage(request, *args, **kwargs):
    template_name = "home.html"
    print(request.POST)
    form = EmailForm(request.POST or None)
    context = {
        'form': form,
        'message': ""
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        with transaction.atomic():
            try:
                email_obj, created = Email.objects.get_or_create(
                    email=email
                )
                obj = EmailVerificationEvent.objects.create(
                    parent=email_obj,
                    email=email,
                )
            except Exception as e:
                print(f"Error: {e}")
        context['form'] = EmailForm()
        context['message'] = "Success! Check your email for verification."
    else:
        print(form.errors)
    return render(request, template_name, context)