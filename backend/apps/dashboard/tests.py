from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class DashboardSummaryTests(APITestCase):
    def test_empty_dashboard_has_zero_totals(self):
        user = User.objects.create_user("dashboard-user", password="StrongPass123!")
        self.client.force_authenticate(user)
        response = self.client.get("/api/v1/dashboard/summary/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["homes"], 0)
        self.assertEqual(payload["devices"]["total"], 0)
        self.assertEqual(payload["consumption24h"]["energyKwh"], 0.0)
