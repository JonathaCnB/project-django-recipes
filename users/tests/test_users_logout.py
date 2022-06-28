from django.test import TestCase
from django.urls import reverse
from users.models import User


class UserLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        str_password = "pass"
        User.objects.create_user(
            username="my_user",
            first_name="my_user",
            password=str_password,
        )
        self.client.login(username="my_user", password=str_password)
        resp = self.client.get(reverse("users:logout"), follow=True)

        msg = "Solicitação de logout inválida"

        self.assertIn(msg, resp.content.decode("utf-8"))

    def test_user_tries_to_logout_another_user(self):
        str_password = "pass"
        User.objects.create_user(
            username="my_user",
            first_name="my_user",
            password=str_password,
        )
        self.client.login(username="my_user", password=str_password)
        resp = self.client.post(
            reverse("users:logout"),
            data={"username": "anotheruser"},
            follow=True,
        )

        msg = "Logout de usuário inválido"

        self.assertIn(msg, resp.content.decode("utf-8"))

    def test_user_can_logout_successfully(self):
        str_password = "pass"
        User.objects.create_user(
            username="my_user",
            first_name="my_user",
            password=str_password,
        )
        self.client.login(username="my_user", password=str_password)
        resp = self.client.post(
            reverse("users:logout"),
            data={"username": "my_user"},
            follow=True,
        )

        msg = "Deslogado com sucesso!"

        self.assertIn(msg, resp.content.decode("utf-8"))
