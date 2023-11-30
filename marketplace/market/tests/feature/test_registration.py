from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from market.models import CustomUser


class RegisterUserTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # user gets to the home page
    def test_home_url_opens(self):
        self.selenium.get(f'{self.live_server_url}/home/')

    # user clicks link Register and gets to the register_user page
    def test_click_register_link(self):
        self.selenium.get(f'{self.live_server_url}/home/')

        register_link = self.selenium.find_element(By.LINK_TEXT, "Register")

        register_link.click()
        self.selenium.implicitly_wait(10)

        expected_url = f'{self.live_server_url}/register_user/'
        current_url = self.selenium.current_url
        self.assertEqual(current_url, expected_url, f'Expected URL: {expected_url}, but got: {current_url}')

    # user registers themselves
    def test_register_user(self):
        self.selenium.get(f'{self.live_server_url}/register_user/')

        email_field = self.selenium.find_element(By.NAME, "email")
        password_field1 = self.selenium.find_element(By.NAME, "password1")
        password_field2 = self.selenium.find_element(By.NAME, "password2")

        email_field.send_keys("testuser@example.com")
        password_field1.send_keys("securepassword123")
        password_field2.send_keys("securepassword123")

        submit_button = self.selenium.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        self.selenium.implicitly_wait(10)
        registered_user = CustomUser.objects.get(email="testuser@example.com")
        self.assertTrue(registered_user)

    # user gets back to home page after registratin and see a success message
    def test_user_redirects_to_home_after_registration(self):
        self.selenium.get(f'{self.live_server_url}/register_user/')

        email_field = self.selenium.find_element(By.NAME, "email")
        password_field1 = self.selenium.find_element(By.NAME, "password1")
        password_field2 = self.selenium.find_element(By.NAME, "password2")

        email_field.send_keys("testuser@example.com")
        password_field1.send_keys("securepassword123")
        password_field2.send_keys("securepassword123")

        submit_button = self.selenium.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        self.selenium.implicitly_wait(10)
        registered_user = CustomUser.objects.get(email="testuser@example.com")
        self.assertTrue(registered_user)

        self.selenium.implicitly_wait(10)
        expected_url = f'{self.live_server_url}/home/'
        current_url = self.selenium.current_url
        self.assertEqual(current_url, expected_url, f'Expected URL: {expected_url}, but got: {current_url}')
