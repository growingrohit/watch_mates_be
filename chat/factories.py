import factory
from factory.django import DjangoModelFactory

from accounts.factories import ProfileFactory, UserFactory
from chat.models import (
    LinkMessage,
    MediaMessage,
    MediaKind,
    MessageKind,
    MessageReceipt,
    PlatformKind,
    TextMessage,
    Thread,
    ThreadKind,
    ThreadMember,
    ThreadMessage,
)

from common.factories import AuditFactoryMixin


class ThreadFactory(AuditFactoryMixin, DjangoModelFactory):
    class Meta:
        model = Thread

    name = factory.Faker("sentence", nb_words=3)
    profile_image = factory.Faker("image_url")
    kind = ThreadKind.DIRECT


class ThreadMemberFactory(AuditFactoryMixin, DjangoModelFactory):
    class Meta:
        model = ThreadMember

    thread = factory.SubFactory(ThreadFactory)
    member = factory.SubFactory(ProfileFactory)


class ThreadMessageFactory(AuditFactoryMixin, DjangoModelFactory):
    class Meta:
        model = ThreadMessage

    thread = factory.SubFactory(ThreadFactory)
    kind = MessageKind.TEXT
    delivered_time = None


class TextMessageFactory(ThreadMessageFactory):
    class Meta:
        model = TextMessage

    kind = MessageKind.TEXT
    content = factory.Faker("sentence")


class MediaMessageFactory(ThreadMessageFactory):
    class Meta:
        model = MediaMessage

    kind = MessageKind.MEDIA
    media_url = factory.Faker("image_url")
    media_kind = MediaKind.IMAGE


class LinkMessageFactory(ThreadMessageFactory):
    class Meta:
        model = LinkMessage

    kind = MessageKind.LINK
    link = factory.Faker("url")
    platform = PlatformKind.WEB


class MessageReceiptFactory(AuditFactoryMixin, DjangoModelFactory):
    class Meta:
        model = MessageReceipt

    message = factory.SubFactory(TextMessageFactory)
    receiver = factory.SubFactory(ProfileFactory)
    reaction = ""
