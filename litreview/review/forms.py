from django import forms
from django.core.exceptions import ValidationError
from .models import Ticket
from .models import Review
from django.contrib.auth.models import User
from .forms_settings import PASSWORD_MIN_LENGTH
from .forms_settings import PASSWORD_MAX_LENGTH
from .forms_settings import ERRORS_LOGIN_FORM
from .forms_settings import ERRORS_REGISTRATION_FORM
from .forms_settings import ERRORS_SUBSCRIPTION_FORM
from .forms_settings import SPECIAL_SYMBOL
from .forms_settings import CHOICES_REVIEW_FORM


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "login-block__form__control-text",
            'placeholder': "Nom d'utilisateur"}), required=True)
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': "login-block__form__control-text",
            'placeholder': "Mot de passe"}), required=True)

    def clean_password(self):
        username = self.cleaned_data['username']
        try:
            user_test = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(ERRORS_LOGIN_FORM[0])
        else:
            password_test = self.cleaned_data['password']
        if user_test.check_password(password_test):
            return self.cleaned_data['password']
        else:
            raise ValidationError(ERRORS_LOGIN_FORM[1])


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'registration-block__form__control-text',
        'placeholder': "Nom d'utilisateur"}),
        required=True, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'registration-block__form__control-text',
        'placeholder': "Mot de passe"}),
        required=True, max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'registration-block__form__control-text',
        'placeholder': "Confirmer mot de passe"}),
        required=True, max_length=100)

    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            User.objects.get(username=user)
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise ValidationError(ERRORS_REGISTRATION_FORM[0])

    def clean_confirm_password(self):
        password_test = self.cleaned_data['password']
        confirm_password_test = self.cleaned_data['confirm_password']
        if password_test and confirm_password_test:
            if password_test != confirm_password_test:
                raise ValidationError(ERRORS_REGISTRATION_FORM[1])
            else:
                if len(password_test) < PASSWORD_MIN_LENGTH:
                    raise ValidationError(ERRORS_REGISTRATION_FORM[2])
                if len(password_test) > PASSWORD_MAX_LENGTH:
                    raise ValidationError(ERRORS_REGISTRATION_FORM[3])
                if password_test.isdigit():
                    raise ValidationError(ERRORS_REGISTRATION_FORM[4])
                if not any(char.isdigit() for char in password_test):
                    raise ValidationError(ERRORS_REGISTRATION_FORM[5])
                if not any(char.isupper() for char in password_test):
                    raise ValidationError(ERRORS_REGISTRATION_FORM[6])
                if not any(char.islower() for char in password_test):
                    raise ValidationError(ERRORS_REGISTRATION_FORM[7])
                if not any(char in SPECIAL_SYMBOL for char in password_test):
                    raise ValidationError(ERRORS_REGISTRATION_FORM[8])


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
          'title': forms.TextInput(attrs={'class': 'ticket_body__form__form'}),
          'description': forms.Textarea(attrs={'class': 'ticket_body__form__form'}),
          'image': forms.TextInput(attrs={'class': 'ticket_body__form__form',
            'placeholder': "facultatif, lien URL uniquement"})}
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        widgets = {
          'headline': forms.TextInput(attrs={'class': 'review_body__form__form'}),
          'body': forms.Textarea(attrs={'class': 'review_body__form__form'}),
          'rating':forms.RadioSelect(choices=CHOICES_REVIEW_FORM,
            attrs={'class': 'review_body__form__form_radio'})}
         


class SubsriptionForm(forms.Form):
    username = forms.CharField(
        label='Nom', max_length=100,
        widget=forms.TextInput(attrs={'class': 'subscription_body__form__form',
            'placeholder': "Entrer le nom d'un utilisateur"}),
            required=True)

    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            User.objects.get(username=user)
        except User.DoesNotExist:
            raise ValidationError(ERRORS_SUBSCRIPTION_FORM[0])
        else:
            return self.cleaned_data['username']
