from common import SeleniumTest

class LoginTests(SeleniumTest):
    fixtures = ['unprivileged-user.json']

    def test_login_both_empty(self):
        self.get('/accounts/login/')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('This field is required.', body.text)

    def test_login_empty_pass(self):
        self.get('/accounts/login/')
        user = self.driver.find_element_by_name("username")
        user.send_keys('baseuser')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('This field is required.', body.text)

    def test_login_incorrect_pass(self):
        self.get('/accounts/login/')
        user = self.driver.find_element_by_name("username")
        user.send_keys('baseuser')
        passwd = self.driver.find_element_by_name("password")
        passwd.send_keys('wrong')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('Please enter a correct username and password', body.text)

    def test_login_correct_pass(self):
        self.get('/accounts/login/')
        user = self.driver.find_element_by_name("username")
        user.send_keys('baseuser')
        passwd = self.driver.find_element_by_name("password")
        passwd.send_keys('secret')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('Your profile', body.text)
        self.assertNotIn('Administration', body.text)

