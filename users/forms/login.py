from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "placeholder": "Digite e-mail cadastrado",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Digite sua senha",
            },
        ),
    )
