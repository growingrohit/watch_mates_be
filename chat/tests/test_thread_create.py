from django.urls import reverse
from rest_framework import status

from chat.models import Thread, ThreadMember
from chat.tests.base import ChatAPITestCase


class ThreadCreateAPITestCase(ChatAPITestCase):
    url = reverse("threads")

    @classmethod
    def setUpTestData(cls):
        cls.user, cls.profile = cls.create_user_with_profile(username="createuser")
        cls.member_user, cls.member_profile = cls.create_user_with_profile(
            username="memberuser"
        )

    def test_create_thread_success(self):
        self.authenticate(self.user)
        payload = {
            "name": "New group",
            "kind": "group",
            "profile_image": "https://example.com/thread.png",
            "members": [str(self.member_profile.id)],
        }
        response = self.client.put(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Thread created successfully.")
        self.assertEqual(response.data["data"]["name"], "New group")
        self.assertEqual(response.data["data"]["kind"], "group")

        thread = Thread.objects.get(id=response.data["data"]["id"])
        member_profile_ids = set(
            ThreadMember.objects.filter(thread=thread, is_active=True).values_list(
                "member_id", flat=True
            )
        )
        self.assertIn(self.profile.id, member_profile_ids)
        self.assertIn(self.member_profile.id, member_profile_ids)

    def test_create_thread_invalid_member_id(self):
        self.authenticate(self.user)
        payload = {
            "name": "Bad members",
            "members": ["00000000-0000-0000-0000-000000000099"],
        }
        response = self.client.put(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("members", response.data)

    def test_create_thread_requires_authentication(self):
        response = self.client.put(
            self.url,
            {"name": "No auth"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
