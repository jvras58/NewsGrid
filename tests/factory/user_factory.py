import factory

from app.models.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    hashed_password = factory.Faker("password")
    created_at = factory.Faker("date_time")
