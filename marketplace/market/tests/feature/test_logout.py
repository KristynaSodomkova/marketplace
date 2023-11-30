from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from market.models import CustomUser


class LoginUserTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Create a test user
        CustomUser.objects.create_user(email='agatha.christie@gmail.com', password='securepassword123')

    # user logs in and logs out
    def test_logout(self):
        self.selenium.get(f'{self.live_server_url}/login_user/')

        email_field = self.selenium.find_element(By.NAME, "email")
        password_field = self.selenium.find_element(By.NAME, "password")

        email_field.send_keys("agatha.christie@gmail.com")
        password_field.send_keys("securepassword123")

        submit_button = self.selenium.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        success_message = self.selenium.find_element(By.CLASS_NAME, "success")
        self.assertIn("Login successful", success_message.text)

        logout_link = self.selenium.find_element(By.LINK_TEXT, "Logout")

        logout_link.click()
        self.selenium.implicitly_wait(10)
        logout_link = self.selenium.find_element(By.LINK_TEXT, "Login")
        self.assertIsNotNone(logout_link)
