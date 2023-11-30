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

    # user gets to the home page
    def test_home_url_opens(self):
        self.selenium.get(f'{self.live_server_url}/home/')

    # user clicks link Login and gets to the login_user page
    def test_click_login_link(self):
        self.selenium.get(f'{self.live_server_url}/home/')

        login_link = self.selenium.find_element(By.LINK_TEXT, "Login")

        login_link.click()
        self.selenium.implicitly_wait(10)

        expected_url = f'{self.live_server_url}/login_user/'
        current_url = self.selenium.current_url
        self.assertEqual(current_url, expected_url, f'Expected URL: {expected_url}, but got: {current_url}')

    # user loggs in themselves and see an option for logout and success message and is redirected home
    def test_login_user(self):
        self.selenium.get(f'{self.live_server_url}/login_user/')

        email_field = self.selenium.find_element(By.NAME, "email")
        password_field = self.selenium.find_element(By.NAME, "password")

        email_field.send_keys("agatha.christie@gmail.com")
        password_field.send_keys("securepassword123")

        submit_button = self.selenium.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        self.selenium.implicitly_wait(10)
        logout_link = self.selenium.find_element(By.LINK_TEXT, "Logout")
        self.assertIsNotNone(logout_link)

        success_message = self.selenium.find_element(By.CLASS_NAME, "success")
        self.assertIn("Login successful", success_message.text)

    # user gets back to home page after login
    def test_user_redirects_to_home_after_login(self):
        self.selenium.get(f'{self.live_server_url}/login_user/')

        email_field = self.selenium.find_element(By.NAME, "email")
        password_field = self.selenium.find_element(By.NAME, "password")

        email_field.send_keys("agatha.christie@gmail.com")
        password_field.send_keys("securepassword123")

        submit_button = self.selenium.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        self.selenium.implicitly_wait(10)
        expected_url = f'{self.live_server_url}/home/'
        current_url = self.selenium.current_url
        self.assertEqual(current_url, expected_url, f'Expected URL: {expected_url}, but got: {current_url}')
