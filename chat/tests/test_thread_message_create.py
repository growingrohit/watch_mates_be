from django.urls import reverse
from rest_framework import status

from chat.factories import ThreadFactory, ThreadMemberFactory
from chat.models import LinkMessage, MediaMessage, TextMessage
from chat.tests.base import ChatAPITestCase


class ThreadMessageCreateAPITestCase(ChatAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, cls.profile = cls.create_user_with_profile(username="msgcreateuser")
        cls.other_user, cls.other_profile = cls.create_user_with_profile(
            username="msgcreateother"
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

    def _url(self, thread_id):
        return reverse("thread-messages", kwargs={"thread_id": thread_id})

    def test_create_text_message_success(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.thread.id),
            {"kind": "text", "content": "Hello thread"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Message created successfully.")
        self.assertEqual(response.data["data"]["kind"], "text")
        self.assertEqual(response.data["data"]["content"], "Hello thread")
        self.assertEqual(response.data["data"]["message_type"], "TextMessage")

        message = TextMessage.objects.get(id=response.data["data"]["id"])
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.last_message_id, message.id)

    def test_create_media_message_success(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.thread.id),
            {
                "kind": "media",
                "media_url": "https://example.com/clip.mp4",
                "media_kind": "video",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["message_type"], "MediaMessage")
        self.assertTrue(MediaMessage.objects.filter(id=response.data["data"]["id"]).exists())

    def test_create_link_message_success(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.thread.id),
            {
                "kind": "link",
                "link": "https://youtube.com/watch?v=test",
                "platform": "youtube",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["message_type"], "LinkMessage")
        self.assertTrue(LinkMessage.objects.filter(id=response.data["data"]["id"]).exists())

    def test_create_message_missing_content_for_text(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.thread.id),
            {"kind": "text"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)

    def test_create_message_thread_not_accessible(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.private_thread.id),
            {"kind": "text", "content": "Nope"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_message_requires_authentication(self):
        response = self.client.put(
            self._url(self.thread.id),
            {"kind": "text", "content": "No auth"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
