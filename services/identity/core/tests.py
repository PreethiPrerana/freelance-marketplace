from django.test import TestCase
from django.contrib.auth import get_user_model
class UserModelTests(TestCase):
 def test_email_is_login_identifier_and_role_is_stored(self):
  u=get_user_model().objects.create_user(username="freelancer1",email="f@example.com",password="A-strong-password-123",role="freelancer")
  self.assertEqual(u.role,"freelancer"); self.assertTrue(u.check_password("A-strong-password-123"))
