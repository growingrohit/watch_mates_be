from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import DEFAULT_PASSWORD, UserFactory
from accounts.models import Profile

User = get_user_model()


class UserProfileCreateAPITestCase(APITestCase):
    url = reverse("user-profile-create")

    def _valid_payload(self, **overrides):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": DEFAULT_PASSWORD,
            "first_name": "New",
            "last_name": "User",
            "country_code": "+91",
            "mobile_number": "9876543210",
            "display_name": "New User",
            "bio": "Hello from tests",
            "avatar": "https://example.com/avatar.png",
        }
        payload.update(overrides)
        return payload

    def test_create_user_and_profile_success(self):
        response = self.client.post(self.url, self._valid_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["message"],
            "User and profile created successfully.",
        )

        user = User.objects.get(username="newuser")
        self.assertEqual(response.data["data"]["id"], str(user.id))
        self.assertEqual(response.data["data"]["username"], "newuser")
        self.assertEqual(response.data["data"]["email"], "newuser@example.com")
        self.assertEqual(response.data["data"]["full_name"], "New User")

        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.display_name, "New User")
        self.assertEqual(profile.bio, "Hello from tests")
        self.assertEqual(profile.avatar, "https://example.com/avatar.png")
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_create_user_with_minimal_fields(self):
        payload = {
            "username": "minimaluser",
            "password": DEFAULT_PASSWORD,
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="minimaluser")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.display_name, "")
        self.assertEqual(profile.bio, "")
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_create_user_duplicate_username(self):
        UserFactory(username="existinguser")

        response = self.client.post(
            self.url,
            self._valid_payload(username="existinguser"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_create_user_duplicate_email(self):
        UserFactory(username="userone", email="duplicate@example.com")

        response = self.client.post(
            self.url,
            self._valid_payload(
                username="usertwo",
                email="duplicate@example.com",
                mobile_number="9876543211",
            ),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_user_duplicate_mobile_number(self):
        UserFactory(username="userone", mobile_number="9876543210")

        response = self.client.post(
            self.url,
            self._valid_payload(
                username="usertwo",
                email="another@example.com",
                mobile_number="9876543210",
            ),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mobile_number", response.data)

    def test_create_user_password_too_short(self):
        response = self.client.post(
            self.url,
            self._valid_payload(password="short"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_create_user_missing_username(self):
        payload = self._valid_payload()
        del payload["username"]

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_create_user_missing_password(self):
        payload = self._valid_payload()
        del payload["password"]

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
