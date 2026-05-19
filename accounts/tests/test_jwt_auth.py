from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.views import APIView

from accounts.factories import DEFAULT_PASSWORD, UserFactory


class ProtectedSampleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username})


class JWTAuthTestCase(APITestCase):
    request_factory = APIRequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="jwtuser", password=DEFAULT_PASSWORD)

    def test_token_refresh(self):
        login_response = self.client.post(
            reverse("login"),
            {"username": "jwtuser", "password": DEFAULT_PASSWORD},
            format="json",
        )
        refresh_token = login_response.data["tokens"]["refresh"]

        response = self.client.post(
            reverse("token-refresh"),
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_protected_endpoint_requires_authentication(self):
        request = self.request_factory.get("/protected/")
        response = ProtectedSampleAPIView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_token_grants_authentication(self):
        login_response = self.client.post(
            reverse("login"),
            {"username": "jwtuser", "password": DEFAULT_PASSWORD},
            format="json",
        )
        access_token = login_response.data["tokens"]["access"]

        request = self.request_factory.get("/protected/")
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        response = ProtectedSampleAPIView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "jwtuser")
