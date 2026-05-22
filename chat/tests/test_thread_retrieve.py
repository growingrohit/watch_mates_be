from django.urls import reverse
from rest_framework import status

from chat.factories import ThreadFactory, ThreadMemberFactory
from chat.tests.base import ChatAPITestCase


class ThreadRetrieveAPITestCase(ChatAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, cls.profile = cls.create_user_with_profile(username="retrieveuser")
        cls.other_user, cls.other_profile = cls.create_user_with_profile(
            username="retrieveother"
        )

        cls.thread = ThreadFactory(
            name="Retrieve me",
            created_by=cls.user,
            updated_by=cls.user,
        )
        ThreadMemberFactory(
            thread=cls.thread,
            member=cls.profile,
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.private_thread = ThreadFactory(
            created_by=cls.other_user,
            updated_by=cls.other_user,
        )
        ThreadMemberFactory(
            thread=cls.private_thread,
            member=cls.other_profile,
            created_by=cls.other_user,
            updated_by=cls.other_user,
        )

    def _url(self, thread_id):
        return reverse("thread-detail", kwargs={"pk": thread_id})

    def test_retrieve_thread_success(self):
        self.authenticate(self.user)
        response = self.client.get(self._url(self.thread.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Thread retrieved successfully.")
        self.assertEqual(response.data["data"]["id"], str(self.thread.id))
        self.assertEqual(response.data["data"]["name"], "Retrieve me")
        self.assertTrue(len(response.data["data"]["members"]) >= 1)

    def test_retrieve_thread_not_found_for_non_member(self):
        self.authenticate(self.user)
        response = self.client.get(self._url(self.private_thread.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_thread_requires_authentication(self):
        response = self.client.get(self._url(self.thread.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
