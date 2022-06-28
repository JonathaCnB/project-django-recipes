from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized
from users.forms import RegisterForm


class UserRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ("first_name", "Digite seu nome aqui"),
            ("last_name", "Digite seu sobrenome aqui"),
            ("email", "Digite seu melhor e-mail"),
            ("password", "Digite uma senha forte"),
            ("password_confirm", "Repita sua senha"),
        ]
    )
    def test_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            ("email", "Digite seu melhor e-mail"),
            ("password", "Sua senha deve conter no minimo 8 digitos"),
        ]
    )
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand(
        [
            ("first_name", "Nome"),
            ("last_name", "Sobrenome"),
            ("email", "E-mail"),
            ("password", "Senha"),
            ("password_confirm", "Confirmação de senha"),
        ]
    )
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class UserRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "username",
            "first_name": "first",
            "last_name": "last",
            "email": "t@t.com",
            "password": "Str0ngPassword",
            "password_confirm": "Str0ngPassword",
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand(
        [
            ("password_confirm", "É necessário confirmar a senha"),
            ("password", "Por favor digite uma senha válida"),
            ("email", "Por favor digite um e-mail válido"),
            ("first_name", "Por favor digite um nome válido"),
            ("last_name", "Por favor digite um sobrenome válido"),
        ]
    )
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("users:register_create")
        resp = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, resp.content.decode("utf-8"))

    def test_password_field_min_length_shout_be_8(self):
        self.form_data["password"] = "Str0ng"
        url = reverse("users:register_create")
        resp = self.client.post(url, data=self.form_data, follow=True)
        msg = "Senha não pode conter menos que 8 caracteres"
        self.assertIn(msg, resp.context["form"].errors.get("password"))
        self.assertIn(msg, resp.content.decode("utf-8"))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data["password"] = "abcdefgh"
        url = reverse("users:register_create")
        resp = self.client.post(url, data=self.form_data, follow=True)
        msg = "As condições necessarias não foram atendidas"
        self.assertIn(msg, resp.context["form"].errors.get("password"))
        self.assertIn(msg, resp.content.decode("utf-8"))

    def test_password_field_and_password_confirm_are_equal(self):
        self.form_data["password"] = "abcdefgh"
        self.form_data["password_confirm"] = "Abcdefgh"
        url = reverse("users:register_create")
        resp = self.client.post(url, data=self.form_data, follow=True)
        msg = "Campos de senha não são identicos"
        self.assertIn(msg, resp.context["form"].errors.get("password"))
        self.assertIn(msg, resp.content.decode("utf-8"))

        self.form_data["password"] = "Str0ngPassword"
        self.form_data["password_confirm"] = "Str0ngPassword"
        url = reverse("users:register_create")
        resp = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, resp.content.decode("utf-8"))

    def test_send_get_request_to_registration_create_view_return_404(self):
        url = reverse("users:register_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse("users:register_create")
        self.client.post(url, data=self.form_data, follow=True)
        resp = self.client.post(url, data=self.form_data, follow=True)
        msg = "E-mail já em uso"
        self.assertIn(msg, resp.context["form"].errors.get("email"))
        self.assertIn(msg, resp.content.decode("utf-8"))

    def test_user_created_can_login(self):
        url = reverse("users:register_create")
        self.form_data.update(
            {"password": "@Bcd12345", "password_confirm": "@Bcd12345"}
        )
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username="t@t.com",
            password="@Bcd12345",
        )
        self.assertTrue(is_authenticated)

    def test_user_created_first_name_in_password(self):
        url = reverse("users:register_create")
        self.form_data.update(
            {
                "first_name": "John",
                "password": "John@Bcd12345",
                "password_confirm": "John@Bcd12345",
            }
        )
        resp = self.client.post(url, data=self.form_data, follow=True)

        msg = "Não digite John no campo senha"

        self.assertIn(msg, resp.context["form"].errors.get("password"))
        self.assertIn(msg, resp.content.decode("utf-8"))
