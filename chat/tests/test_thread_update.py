from django.urls import reverse
from rest_framework import status

from chat.factories import ThreadFactory, ThreadMemberFactory
from chat.models import ThreadMember
from chat.tests.base import ChatAPITestCase


class ThreadUpdateAPITestCase(ChatAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, cls.profile = cls.create_user_with_profile(username="updateuser")
        cls.other_user, cls.other_profile = cls.create_user_with_profile(
            username="updateother"
        )
        cls.new_member_user, cls.new_member_profile = cls.create_user_with_profile(
            username="newmember"
        )

        cls.thread = ThreadFactory(
            name="Old name",
            kind="direct",
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

    def test_update_thread_success(self):
        self.authenticate(self.user)
        payload = {
            "name": "Updated name",
            "kind": "group",
            "members": [str(self.new_member_profile.id)],
        }
        response = self.client.put(self._url(self.thread.id), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Thread updated successfully.")
        self.assertEqual(response.data["data"]["name"], "Updated name")
        self.assertEqual(response.data["data"]["kind"], "group")

        active_member_ids = set(
            ThreadMember.objects.filter(
                thread=self.thread, is_active=True
            ).values_list("member_id", flat=True)
        )
        self.assertIn(self.new_member_profile.id, active_member_ids)

    def test_update_thread_not_found_for_non_member(self):
        self.authenticate(self.user)
        response = self.client.put(
            self._url(self.private_thread.id),
            {"name": "Hacked"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_thread_requires_authentication(self):
        response = self.client.put(
            self._url(self.thread.id),
            {"name": "No auth"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
