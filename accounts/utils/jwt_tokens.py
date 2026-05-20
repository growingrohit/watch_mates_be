from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def build_user_payload(user):
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
    }


def build_auth_response_data(message, user):
    return {
        "message": message,
        "data": build_user_payload(user),
        "tokens": get_tokens_for_user(user),
    }
