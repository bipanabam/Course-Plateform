from django import forms

from . import services, css

from .models import Email

class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'id': "email-login-input",
                'class': css.form_input_class,
                'placeholder': "Enter your email"
            }
        )
    )
    # class Meta:
    #     model = Email
    #     fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        not_verified = services.verify_email(email)
        if not_verified:
            raise forms.ValidationError("Invalid email. "
            "Please try again.")
        return email