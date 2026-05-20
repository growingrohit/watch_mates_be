from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import DEFAULT_PASSWORD, UserFactory


class LoginAPITestCase(APITestCase):
    url = reverse("login")

    @classmethod
    def setUpTestData(cls):
        cls.password = DEFAULT_PASSWORD
        cls.user = UserFactory(
            username="loginuser",
            email="loginuser@example.com",
            first_name="Login",
            last_name="User",
            password=cls.password,
        )

    def test_login_success(self):
        response = self.client.post(
            self.url,
            {"username": "loginuser", "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login successful.")
        self.assertEqual(response.data["data"]["username"], "loginuser")
        self.assertEqual(response.data["data"]["email"], "loginuser@example.com")
        self.assertEqual(response.data["data"]["full_name"], "Login User")
        self.assertEqual(str(self.user.id), response.data["data"]["id"])
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_login_user_does_not_exist(self):
        response = self.client.post(
            self.url,
            {"username": "unknown_user", "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "User does not exist.")

    def test_login_invalid_password(self):
        response = self.client.post(
            self.url,
            {"username": "loginuser", "password": "wrongpassword"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Password is invalid.")

    def test_login_missing_username(self):
        response = self.client.post(
            self.url,
            {"password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_login_missing_password(self):
        response = self.client.post(
            self.url,
            {"username": "loginuser"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
