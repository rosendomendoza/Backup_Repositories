import pytest
from backup.models.user import User
from django.db import IntegrityError


@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create(username="testuser",
                               github_url="https://github.com/testuser")
    assert user.username == "testuser"
    assert user.github_url == "https://github.com/testuser"


@pytest.mark.django_db
def test_create_user_duplicate_username():
    User.objects.create(username="testuser",
                        github_url="https://github.com/testuser")
    with pytest.raises(IntegrityError):
        User.objects.create(username="testuser",
                            github_url="https://github.com/duplicateuser")


@pytest.mark.django_db
def test_user_string_representation():
    user = User.objects.create(username="testuser",
                               github_url="https://github.com/testuser")
    assert str(user) == "testuser"
