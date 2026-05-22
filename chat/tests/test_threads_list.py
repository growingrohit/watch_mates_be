from django.urls import reverse
from rest_framework import status

from chat.factories import ThreadFactory, ThreadMemberFactory
from chat.tests.base import ChatAPITestCase


class ThreadsListAPITestCase(ChatAPITestCase):
    url = reverse("threads")

    @classmethod
    def setUpTestData(cls):
        cls.user, cls.profile = cls.create_user_with_profile(username="threadowner")
        cls.other_user, cls.other_profile = cls.create_user_with_profile(
            username="otheruser"
        )

        cls.owned_thread = ThreadFactory(
            name="My thread",
            created_by=cls.user,
            updated_by=cls.user,
        )
        ThreadMemberFactory(
            thread=cls.owned_thread,
            member=cls.profile,
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.member_thread = ThreadFactory(
            name="Shared thread",
            created_by=cls.other_user,
            updated_by=cls.other_user,
        )
        ThreadMemberFactory(
            thread=cls.member_thread,
            member=cls.profile,
            created_by=cls.other_user,
            updated_by=cls.other_user,
        )

        cls.hidden_thread = ThreadFactory(
            name="Hidden thread",
            created_by=cls.other_user,
            updated_by=cls.other_user,
        )
        ThreadMemberFactory(
            thread=cls.hidden_thread,
            member=cls.other_profile,
            created_by=cls.other_user,
            updated_by=cls.other_user,
        )

    def test_list_threads_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_threads_returns_accessible_threads_only(self):
        self.authenticate(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Threads retrieved successfully.")

        thread_ids = {item["id"] for item in response.data["data"]}
        self.assertIn(str(self.owned_thread.id), thread_ids)
        self.assertIn(str(self.member_thread.id), thread_ids)
        self.assertNotIn(str(self.hidden_thread.id), thread_ids)

    def test_list_threads_empty_for_user_without_membership(self):
        outsider, _ = self.create_user_with_profile(username="outsider")
        self.authenticate(outsider)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], [])
