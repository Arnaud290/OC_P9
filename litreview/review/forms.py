"""
Forms management module
"""
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Ticket
from .models import Review
from .forms_settings import PASSWORD_MIN_LENGTH
from .forms_settings import PASSWORD_MAX_LENGTH
from .forms_settings import ERRORS_LOGIN_FORM
from .forms_settings import ERRORS_REGISTRATION_FORM
from .forms_settings import ERRORS_SUBSCRIPTION_FORM
from .forms_settings import SPECIAL_SYMBOL
from .forms_settings import CHOICES_REVIEW_FORM


class LoginForm(forms.Form):
    """
    class from the login form
    """
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': "login_block__form__form",
            'placeholder': "Nom d'utilisateur"}), required=True)
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': "login_block__form__form",
            'placeholder': "Mot de passe"}), required=True)

    def clean_password(self):
        """
        Password verification function.
        If the username or password does not allow connection,
        it returns a validation error
        """
        username = self.cleaned_data['username']
        try:
            user_test = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(ERRORS_LOGIN_FORM[0])
        password_test = self.cleaned_data['password']
        if user_test.check_password(password_test):
            return self.cleaned_data['password']
        raise ValidationError(ERRORS_LOGIN_FORM[1])


class RegistrationForm(forms.Form):
    """
    Class of the registration form
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'registration_block__form__form',
            'placeholder': "Nom d'utilisateur"}),
        required=True, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'registration_block__form__form',
            'placeholder': "Mot de passe"}),
        required=True, max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'registration_block__form__form',
            'placeholder': "Confirmer mot de passe"}),
        required=True, max_length=100)

    def clean_username(self):
        """
        Name verification function.
        If the name already exists in the database,
        it returns a validation error.
        """
        user = self.cleaned_data['username']
        try:
            User.objects.get(username=user)
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise ValidationError(ERRORS_REGISTRATION_FORM[0])

    def clean_confirm_password(self):
        """
        Password strength verification function
        """
        password_test = self.cleaned_data['password']
        confirm_password_test = self.cleaned_data['confirm_password']
        if password_test and confirm_password_test:
            if password_test != confirm_password_test:
                raise ValidationError(ERRORS_REGISTRATION_FORM[1])
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
    """
    Ticket creation form class
    """
    class Meta:
        """
        Form retrieved from the Ticket model
        """
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'ticket_body__form__form'}),
            'description': forms.Textarea(attrs={'class': 'ticket_body__form__form'}),
            'image': forms.TextInput(attrs={
                'class': 'ticket_body__form__form',
                'placeholder': "facultatif, lien URL uniquement."
            })
        }


class ReviewForm(forms.ModelForm):
    """
    Class of the reviews form
    """
    class Meta:
        """
        Form retrieved from the Review model
        """
        model = Review
        fields = ['headline', 'body', 'rating']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'review_body__form__form'}),
            'body': forms.Textarea(attrs={'class': 'review_body__form__form'}),
            'rating': forms.RadioSelect(
                choices=CHOICES_REVIEW_FORM,
                attrs={'class': 'review_body__form__form_radio'})
        }


class SubsriptionForm(forms.Form):
    """
    Subscription form class
    """
    username = forms.CharField(
        label='Nom', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'subscription_body__form__form',
                'placeholder': "Entrer le nom d'un utilisateur"}), required=True)

    def clean_username(self):
        """
        User name verification function.
        If the requested username does not exist,
        it returns a validation error.
        """
        user = self.cleaned_data['username']
        try:
            User.objects.get(username=user)
        except User.DoesNotExist:
            raise ValidationError(ERRORS_SUBSCRIPTION_FORM[0])
        else:
            return self.cleaned_data['username']
