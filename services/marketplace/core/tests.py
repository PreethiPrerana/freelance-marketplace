from django.test import TestCase
from .models import Job,Proposal
import uuid
class MarketplaceModelTests(TestCase):
 def test_proposal_is_unique_per_freelancer_and_job(self):
  j=Job.objects.create(client_id=uuid.uuid4(),title="API work",description="Build an API",budget=100); uid=uuid.uuid4(); Proposal.objects.create(job=j,freelancer_id=uid,cover_letter="I can help",bid_amount=90)
  with self.assertRaises(Exception): Proposal.objects.create(job=j,freelancer_id=uid,cover_letter="Again",bid_amount=80)
