from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AccountApiTests(APITestCase):
    def test_register_login_and_me(self):
        register = self.client.post(
            "/api/v1/auth/register/",
            {"username": "eco", "email": "eco@example.com", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

        token = self.client.post(
            "/api/v1/auth/token/",
            {"username": "eco", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(token.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.data['access']}")

        me = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me.status_code, status.HTTP_200_OK)
        self.assertEqual(me.data["username"], "eco")
