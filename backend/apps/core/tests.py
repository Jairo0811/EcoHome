from django.test import TestCase
class HealthTests(TestCase):
 def test_health(self):
  r=self.client.get('/api/v1/health/');self.assertEqual(r.status_code,200);self.assertEqual(r.json()['status'],'ok')
 def test_readiness(self):
  r=self.client.get('/api/v1/health/ready/');self.assertEqual(r.status_code,200);self.assertEqual(r.json()['database'],'ok')
