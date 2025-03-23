from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from . import services

from .forms import EmailForm

# Create your views here.
EMAIL_ADDRESS = settings.EMAIL_ADDRESS
def email_token_login_view(request):
    if not request.htmx:
        return redirect("/")
    email_id_in_session = request.session.get('email_id')
    template = "emails/hx/email_form.html"
    
    form = EmailForm(request.POST or None)
    context = {
        'form': form,
        'message': "",
        'show_form': not email_id_in_session
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        services.start_verification_event(email)
        context['form'] = EmailForm()
        context['message'] = f"Success! Check your email for verification from {EMAIL_ADDRESS}."
    else:
        print(form.errors)
    return render(request, template, context)


def verify_email_token_view(request, token):
    did_verify, msg, email_obj = services.verify_token(token)
    if not did_verify:
        try:
            del request.session['email_id']
        except:
            pass
        messages.error(request, msg)
        return redirect("/login/")
    messages.success(request, "Email verified successfully!")
    request.session['email_id'] = f"{email_obj.id}"
    next_url = request.session.get('next_url') or "/"
    if not next_url.startswith("/"):
        next_url = "/"
    return redirect(next_url)