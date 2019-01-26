from .factories import UserFactory, ProfileFactory
import pytest

@pytest.mark.django_db
def test_create_user():
    user = UserFactory()
    assert user.username == 'test_username'

@pytest.mark.django_db
def test_create_profile():
    profile = ProfileFactory()

    assert profile.status == 1
