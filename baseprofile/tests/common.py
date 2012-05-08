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

