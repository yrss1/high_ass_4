from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, SensitiveData


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')


class CustomAuthenticationForm(AuthenticationForm):
    otp_token = forms.CharField(required=False, max_length=6)


class SensitiveDataForm(forms.ModelForm):
    class Meta:
        model = SensitiveData
        fields = ['sensitive_info']

    def clean_sensitive_info(self):
        data = self.cleaned_data['sensitive_info']
        # Add any additional validation here
        return data
