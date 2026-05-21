from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.factories import ProfileFactory, UserFactory


class ChatAPITestCase(APITestCase):
    def authenticate(self, user):
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    @classmethod
    def create_user_with_profile(cls, **user_kwargs):
        user = UserFactory(**user_kwargs)
        profile = ProfileFactory(user=user)
        return user, profile
