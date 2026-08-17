from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Home, HomeMembership

User = get_user_model()


class HomeAccessTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="StrongPass123!")
        self.member = User.objects.create_user("member", password="StrongPass123!")
        self.stranger = User.objects.create_user("stranger", password="StrongPass123!")
        self.home = Home.objects.create(owner=self.owner, name="Casa")
        HomeMembership.objects.create(home=self.home, user=self.member, role=HomeMembership.Role.MEMBER)

    def test_member_can_read_home(self):
        self.client.force_authenticate(self.member)
        response = self.client.get("/api/v1/homes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_stranger_cannot_read_home(self):
        self.client.force_authenticate(self.stranger)
        response = self.client.get("/api/v1/homes/")
        self.assertEqual(response.data["count"], 0)
