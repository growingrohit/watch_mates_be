import factory
from factory.django import DjangoModelFactory

from accounts.models import Profile, User

DEFAULT_PASSWORD = "securepass123"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda index: f"user_{index}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    country_code = "+91"
    mobile_number = factory.Sequence(lambda index: f"9{index:09d}")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        raw_password = extracted or DEFAULT_PASSWORD
        self.set_password(raw_password)
        if create:
            self.save()


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    display_name = factory.Faker("name")
    bio = factory.Faker("sentence")
    avatar = factory.Faker("image_url")
    profile_image = factory.Faker("image_url")
