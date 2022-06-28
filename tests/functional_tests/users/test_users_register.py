from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import UsersBaseTest


class UsersRegisterTest(UsersBaseTest):
    def fill_form_dummy_data(self, web_element):
        fields = web_element.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 8)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form",
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(f"{self.live_server_url}/users/register/")
        form = self.get_form()
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, "email").send_keys("dummy@email.com")
        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(
                form,
                "Digite seu nome aqui",
            )
            first_name_field.send_keys(" ")
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn("Por favor digite um nome válido", form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                form,
                "Digite seu sobrenome aqui",
            )
            last_name_field.send_keys(" ")
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn("Por favor digite um sobrenome válido", form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(
                form,
                "Digite seu melhor e-mail",
            )
            email_field.send_keys(Keys.BACKSPACE * 15)
            email_field.send_keys("email@invalid")
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn("Informe um endereço de email válido.", form.text)

        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, "Digite uma senha forte")
            password2 = self.get_by_placeholder(form, "Repita sua senha")
            password1.send_keys("P@ssw0rd")
            password2.send_keys("P@ssw0rd_Different")
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn("Campos de senha não são identicos", form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(f"{self.live_server_url}/users/register/")
        form = self.get_form()

        self.get_by_placeholder(
            form,
            "Digite seu nome aqui",
        ).send_keys("First Name")
        self.get_by_placeholder(
            form,
            "Digite seu sobrenome aqui",
        ).send_keys("Last Name")
        self.get_by_placeholder(form, "Digite seu melhor e-mail",).send_keys(
            "email@valid.com",
        )
        self.get_by_placeholder(form, "Digite uma senha forte").send_keys(
            "P@ssw0rd1",
        )
        self.get_by_placeholder(form, "Repita sua senha").send_keys(
            "P@ssw0rd1",
        )

        form.submit()

        self.assertIn(
            "Cadastro realizado, por favor faça login.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
