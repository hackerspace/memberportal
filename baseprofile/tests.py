from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

class SeleniumTests(LiveServerTestCase):
    timeout = 2
    def get_url(self, url):
        self.d.get('%s%s' % (self.live_server_url, url))

    def wait_for_body(self):
        WebDriverWait(self.d, self.timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        return self.d.find_element_by_tag_name('body')

    @classmethod
    def setUpClass(cls):
        cls.d = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SeleniumTests, cls).tearDownClass()
        cls.d.quit()

class LoginTests(SeleniumTests):
    fixtures = ['unprivileged-user.json']

    def test_login_both_empty(self):
        self.get_url('/accounts/login/')
        self.d.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('This field is required.', body.text)

    def test_login_empty_pass(self):
        self.get_url('/accounts/login/')
        user = self.d.find_element_by_name("username")
        user.send_keys('baseuser')
        self.d.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('This field is required.', body.text)

    def test_login_incorrect_pass(self):
        self.get_url('/accounts/login/')
        user = self.d.find_element_by_name("username")
        user.send_keys('baseuser')
        passwd = self.d.find_element_by_name("password")
        passwd.send_keys('wrong')
        self.d.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('Please enter a correct username and password', body.text)

    def test_login_correct_pass(self):
        self.get_url('/accounts/login/')
        user = self.d.find_element_by_name("username")
        user.send_keys('baseuser')
        passwd = self.d.find_element_by_name("password")
        passwd.send_keys('secret')
        self.d.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('Your profile', body.text)

