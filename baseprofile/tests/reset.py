import re

from django.core import mail

from common import SeleniumTest

class ResetTests(SeleniumTest):
    fixtures = ['unprivileged-user.json']

    def test_reset_unknown(self):
        self.get('/accounts/password/reset/')
        email = self.driver.find_element_by_name('email')
        email.send_keys('example@example.org')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('Are you sure you\'ve registered?', body.text)

    def test_reset(self):
        self.get('/accounts/password/reset/')
        email = self.driver.find_element_by_name('email')
        email.send_keys('mail@example.org')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('reset successful', body.text)
        self.assertEqual(len(mail.outbox), 1)
        match = re.search(r'http://example.com/accounts/password/reset/confirm/([^/]+)/',
        mail.outbox[0].body)
        self.assertIsNotNone(match)

        key = match.groups(1)
        self.get('/accounts/password/reset/confirm/%s/' % key)
        body = self.wait_for_body()
        self.assertIn('Reset my password', body.text)
        p1 = self.driver.find_element_by_name('new_password1')
        p2 = self.driver.find_element_by_name('new_password2')
        p1.send_keys('password')
        p2.send_keys('password')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('Your password was changed', body.text)

    def test_reset_wrong_key(self):
        self.get('/accounts/password/reset/confirm/1-xxx-6840x316fx9d77f79496/')
        body = self.wait_for_body()
        self.assertIn('link was invalid', body.text)
