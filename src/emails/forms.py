from django import forms

from .models import Email

class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'id': "email-login-input",
                'class': "",
                'placeholder': "Enter your email"
            }
        )
    )
    # class Meta:
    #     model = Email
    #     fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Email.objects.filter(email=email, active=False)
        if qs.exists():
            raise forms.ValidationError("Invalid email. "
            "Please try again.")
        return email