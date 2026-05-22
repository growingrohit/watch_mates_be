from django.urls import reverse
from rest_framework import status

from chat.factories import TextMessageFactory, ThreadFactory, ThreadMemberFactory
from chat.tests.base import ChatAPITestCase


class ThreadMessageUpdateAPITestCase(ChatAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, cls.profile = cls.create_user_with_profile(username="msgupdateuser")
        cls.other_user, cls.other_profile = cls.create_user_with_profile(
            username="msgupdateother"
        )

        cls.thread = ThreadFactory(created_by=cls.user, updated_by=cls.user)
        ThreadMemberFactory(
            thread=cls.thread,
            member=cls.profile,
            created_by=cls.user,
            updated_by=cls.user,
        )
        ThreadMemberFactory(
            thread=cls.thread,
            member=cls.other_profile,
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.own_message = TextMessageFactory(
            thread=cls.thread,
            content="Original",
            created_by=cls.user,
            updated_by=cls.user,
        )
        cls.other_message = TextMessageFactory(
            thread=cls.thread,
            content="Not mine",
            created_by=cls.other_user,
            updated_by=cls.other_user,
        )

    def _url(self, thread_id, message_id):
        return reverse(
            "thread-message-detail",
            kwargs={"thread_id": thread_id, "pk": message_id},
        )

    def test_update_own_message_success(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.thread.id, self.own_message.id),
            {"content": "Updated content"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Message updated successfully.")
        self.assertEqual(response.data["data"]["content"], "Updated content")

        self.own_message.refresh_from_db()
        self.assertEqual(self.own_message.get_real_instance().content, "Updated content")

    def test_update_other_users_message_forbidden(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.thread.id, self.other_message.id),
            {"content": "Hacked"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_message_not_found(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(
                self.thread.id,
                "00000000-0000-0000-0000-000000000099",
            ),
            {"content": "Missing"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_message_requires_authentication(self):
        response = self.client.put(
            self._url(self.thread.id, self.own_message.id),
            {"content": "No auth"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
