import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from backup.models.user import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create(username="testuser",
                               github_url="https://github.com/testuser")


@pytest.mark.django_db
def test_create_user_success(client, mocker):
    mock_validate_github_user = mocker.patch(
        "backup.github_utils.validate_github_user")
    mock_validate_github_user.return_value.status_code = 200
    mock_validate_github_user.return_value.json.return_value = {
        "html_url": "https://github.com/newuser"}
    url = reverse("users-list")
    data = {"username": "newuser"}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"


@pytest.mark.django_db
def test_create_user_already_exists(client, test_user):
    url = reverse("users-list")
    data = {"username": test_user.username}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "User already exists in the database."


@pytest.mark.django_db
def test_fetch_user_success(client, test_user):
    url = reverse("users-fetch-user")
    response = client.get(url, {"username": test_user.username})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == test_user.username


@pytest.mark.django_db
def test_fetch_user_not_found(client):
    url = reverse("users-fetch-user")
    response = client.get(url, {"username": "nonexistent"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data[
               "error"] == "User 'nonexistent' not found in the database."


@pytest.mark.django_db
def test_backup_user_success(client, mocker):
    mock_validate_github_user = mocker.patch(
        "backup.github_utils.validate_github_user")
    mock_validate_github_user.return_value.status_code = 200
    mock_validate_github_user.return_value.json.return_value = {
        "html_url": "https://github.com/backupuser"}
    url = reverse("users-backup-user")
    data = {"username": "backupuser"}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "backupuser"


@pytest.mark.django_db
def test_delete_user_backup_success(client, test_user):
    url = reverse("users-delete-user-backup")
    response = client.delete(url, {"username": test_user.username},
                             format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.filter(username=test_user.username).count() == 0


@pytest.mark.django_db
def test_delete_user_backup_not_found(client):
    url = reverse("users-delete-user-backup")
    response = client.delete(url, {"username": "nonexistent"}, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data[
               "error"] == "User 'nonexistent' not found in the database."
