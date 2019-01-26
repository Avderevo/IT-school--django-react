import factory
from django.contrib.auth.models import User
from ..models import  Profile

class UserFactory(factory.Factory):
    class Meta:
        model = User
    username = 'test_username'
    email = 'test_email@mail.com'

class ProfileFactory(factory.Factory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
