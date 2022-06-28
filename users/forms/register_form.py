from django import forms as frm_django
from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from users.models import User
from utils.django_forms import add_placeholder, strong_password


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = "__all__"


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = "__all__"


class RegisterForm(frm_django.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["last_name"], "Digite seu sobrenome aqui")
        # add_placeholder(self.fields["first_name"], "Digite seu nome aqui")
        # add_placeholder(self.fields["email"], "Digite seu melhor e-mail")

    first_name = frm_django.CharField(
        error_messages={"required": "Por favor digite um nome válido"},
        required=True,
        label="Nome",
        widget=frm_django.TextInput(
            attrs={
                "placeholder": "Digite seu nome aqui",
            }
        ),
    )
    last_name = frm_django.CharField(
        error_messages={"required": "Por favor digite um sobrenome válido"},
        required=True,
        label="Sobrenome",
    )
    email = frm_django.CharField(
        error_messages={"required": "Por favor digite um e-mail válido"},
        required=True,
        widget=frm_django.EmailInput(
            attrs={
                "type": "email",
                "placeholder": "Digite seu melhor e-mail",
            }
        ),
        help_text="Digite seu melhor e-mail",
        label="E-mail",
    )
    password = frm_django.CharField(
        error_messages={
            "required": "Por favor digite uma senha válida",
            "min_length": "Senha não pode conter menos que 8 caracteres",
        },
        required=True,
        label="Senha",
        widget=frm_django.PasswordInput(
            attrs={
                "placeholder": "Digite uma senha forte",
            },
        ),
        help_text="Sua senha deve conter no minimo 8 digitos",
        validators=[strong_password],
        min_length=8,
    )
    password_confirm = frm_django.CharField(
        required=True,
        widget=frm_django.PasswordInput(
            attrs={
                "placeholder": "Repita sua senha",
                "class": "outra-class",
            },
        ),
        error_messages={"required": "É necessário confirmar a senha"},
        label="Confirmação de senha",
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def clean_password(self):
        # data = self.data
        data = self.cleaned_data.get("password")
        name = self.cleaned_data.get("first_name")
        if name and data:
            if name in data:
                raise ValidationError(
                    "Não digite %(name)s no campo senha",
                    code="invalid",
                    params={"name": name},
                )
        return data

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError("E-mail já em uso", code="invalid")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise ValidationError(
                {
                    "password": "Campos de senha não são identicos",
                }
            )
