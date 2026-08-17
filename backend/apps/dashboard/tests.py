from django.test import TestCase


class DashboardSummaryTests(TestCase):
    def test_empty_dashboard_has_zero_totals(self):
        response = self.client.get("/api/v1/dashboard/summary/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["homes"], 0)
        self.assertEqual(payload["devices"]["total"], 0)
        self.assertEqual(payload["consumption24h"]["energyKwh"], 0.0)
