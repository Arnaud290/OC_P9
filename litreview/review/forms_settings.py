PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 40
SPECIAL_SYMBOL = [
    '&', '~', '"', '{', '(', '[', '-', ';', '|',
    '_', ')', '°', ']', '=', '}', '$', '#', 'ù',
    '¨', 'µ', '£', '@']

ERRORS_LOGIN_FORM = [
    "Cet utilisateur n'existe pas",
    "Mot de passe incorrect"]

ERRORS_REGISTRATION_FORM = [
    "Utilisateur déja existant",
    "Les mots de passes ne correspondent pas",
    "Le mot de passe doit avoir au minimum %d caractères"%PASSWORD_MIN_LENGTH,
    "Le mot de passe doit avoir au maximum %d caractères"%PASSWORD_MAX_LENGTH,
    "Le mot de passe ne doit pas être entièrement numérique",
    "Le mot de passe doit contenir au moins un chiffre",
    "Le mot de passe doit contenir au moins une lettre majuscule",
    "Le mot de passe doit contenir au moins une lettre minuscule",
    "Le mot de passe doit avoir au moins un des symboles $ @ # ..."]

ERRORS_SUBSCRIPTION_FORM = [
    "L'utilisateur n'existe pas"]

CHOICES_REVIEW_FORM = [
    ('0', 0), (' 1', 1), (' 2', 2), (' 3', 3), (' 4', 4), (' 5', 5)
]