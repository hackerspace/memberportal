from captcha.fields import CaptchaField
from registration.forms import RegistrationForm

class CaptchaRegistrationForm(RegistrationForm):
    captcha = CaptchaField()
