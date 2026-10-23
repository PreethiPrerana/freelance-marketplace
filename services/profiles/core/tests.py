from django.test import TestCase
from .models import FreelancerProfile
import uuid
class ProfileTests(TestCase):
 def test_profile_has_external_user_uuid(self):
  uid=uuid.uuid4(); p=FreelancerProfile.objects.create(user_id=uid,title="Backend Engineer",skills=["Python"]); self.assertEqual(p.user_id,uid); self.assertIn("Python",p.skills)
