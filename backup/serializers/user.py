from rest_framework import serializers
from ..models.user import User
from .repository import RepositorySerializer


class UserSerializer(serializers.ModelSerializer):
    repositories = RepositorySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'github_url', 'repositories']
