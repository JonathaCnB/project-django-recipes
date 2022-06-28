import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By

from users.models import User

from .base import UsersBaseTest


@pytest.mark.functional_test
class UsersLoginTest(UsersBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        str_password = "pass"
        user = User.objects.create_user(
            username="my_user",
            first_name="my_user",
            password=str_password,
        )
        self.browser.get(self.live_server_url + reverse("users:login"))
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        email_field = self.get_by_placeholder(
            form,
            "Digite e-mail cadastrado",
        )
        password_field = self.get_by_placeholder(form, "Digite sua senha")
        email_field.send_keys(user.username)
        password_field.send_keys(str_password)
        form.submit()
        self.assertIn(
            f"Você está logado com: {user.username}.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse("users:login_create"))

        self.assertIn(
            "Not Found",
            self.browser.find_element(
                By.TAG_NAME,
                "body",
            ).text,
        )

    def test_logout_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse("users:logout"))
        self.assertIn(
            "Login",
            self.browser.find_element(
                By.TAG_NAME,
                "body",
            ).text,
        )

    def test_login_create_raises_user_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse("users:login"))
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        email_field = self.get_by_placeholder(
            form,
            "Digite e-mail cadastrado",
        )
        password_field = self.get_by_placeholder(form, "Digite sua senha")
        email_field.send_keys("invalid_user")
        password_field.send_keys("otherPassword")
        form.submit()
        self.assertIn(
            "Dados invalidos",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )

    def test_login_raises_form_invalid(self):
        self.browser.get(self.live_server_url + reverse("users:login"))
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        email_field = self.get_by_placeholder(
            form,
            "Digite e-mail cadastrado",
        )
        password_field = self.get_by_placeholder(form, "Digite sua senha")
        email_field.send_keys("")
        password_field.send_keys("")
        form.submit()
        self.assertIn(
            "Error ao validar o formulário",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
