from rest_framework import serializers
from ..models.repository import Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name', 'github_url', 'owner']
