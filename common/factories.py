import factory
from accounts.factories import UserFactory


class AuditFactoryMixin:
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.LazyAttribute(lambda obj: obj.created_by)
