import re

from django.core import mail

from common import SeleniumTests

class RegistrationTests(SeleniumTests):
    def test_register_empty(self):
        self.get_url('/accounts/register/')
        self.d.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('This field is required.', body.text)

    def test_register(self):
        self.get_url('/accounts/register/')
        user = self.d.find_element_by_name('username')
        email = self.d.find_element_by_name('email')
        p1 = self.d.find_element_by_name('password1')
        p2 = self.d.find_element_by_name('password2')
        user.send_keys('baseuser')
        email.send_keys('user@example.org')
        p1.send_keys('password')
        p2.send_keys('password')
        self.d.find_element_by_xpath('//button[@type="submit"]').click()
        body = self.wait_for_body()
        self.assertIn('Check your email', body.text)
        self.assertEqual(len(mail.outbox), 1)
        match = re.search(r'http://example.com/accounts/activate/([^/]+)/',
            mail.outbox[0].body)
        self.assertIsNotNone(match)

        key = match.groups(1)
        self.get_url('/accounts/activate/%s/' % key)
        body = self.wait_for_body()
        self.assertIn('Your account is now activated', body.text)

    def test_wrong_key(self):
        self.get_url('/accounts/activate/abcdefgh/')
        body = self.wait_for_body()
        self.assertIn('Activation failed', body.text)
