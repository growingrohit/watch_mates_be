from django.urls import reverse
from rest_framework import status

from chat.factories import TextMessageFactory, ThreadFactory, ThreadMemberFactory
from chat.tests.base import ChatAPITestCase


class ThreadMessagesListAPITestCase(ChatAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, cls.profile = cls.create_user_with_profile(username="msglistuser")
        cls.other_user, cls.other_profile = cls.create_user_with_profile(
            username="msglistother"
        )

        cls.thread = ThreadFactory(created_by=cls.user, updated_by=cls.user)
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

        cls.messages = []
        for index in range(3):
            cls.messages.append(
                TextMessageFactory(
                    thread=cls.thread,
                    content=f"Message {index}",
                    created_by=cls.user,
                    updated_by=cls.user,
                )
            )

    def _url(self, thread_id):
        return reverse("thread-messages", kwargs={"thread_id": thread_id})

    def test_list_messages_paginated_newest_first(self):
        self.authenticate(self.user)
        response = self.client.get(self._url(self.thread.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Messages retrieved successfully.",
        )

        data = response.data["data"]
        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["results"]), 3)
        self.assertEqual(data["results"][0]["content"], "Message 2")
        self.assertEqual(data["results"][-1]["content"], "Message 0")

    def test_list_messages_page_size(self):
        self.authenticate(self.user)
        response = self.client.get(
            self._url(self.thread.id),
            {"page_size": 2},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 2)
        self.assertIsNotNone(response.data["data"]["next"])

    def test_list_messages_not_found_for_non_member(self):
        self.authenticate(self.user)
        response = self.client.get(self._url(self.private_thread.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_messages_requires_authentication(self):
        response = self.client.get(self._url(self.thread.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
