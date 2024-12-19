from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.user import User
from ..models.repository import Repository
from ..serializers.user import UserSerializer
from ..github_utils import validate_github_user

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                name='username',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="The username to fetch from the database",
                required=True
            )
        ],
    )
    @action(detail=False, methods=['get'], url_path='fetch', name='users-fetch')
    def fetch_user(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({"error": "The 'username' parameter is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": f"User '{username}' not found in the database."},
                status=status.HTTP_404_NOT_FOUND)
            
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The username of the user to backup in the database"
                )
            }
        ),
    )
    @action(detail=False, methods=['post'], url_path='backup', name='users-backup')
    def backup_user(self, request):
        username = request.data.get('username')

        if not username:
            return Response({"error": "The 'username' field is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists in the database."},
                            status=status.HTTP_400_BAD_REQUEST)

        response = validate_github_user(username)
        if response.status_code == 200:
            github_data = response.json()
            try:
                user = User.objects.create(username=username,
                                           github_url=github_data['html_url'])
                serializer = self.get_serializer(user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Error creating the user."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                {"error": f"User '{username}' not found on GitHub."},
                status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method='delete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The username of the user to delete from the database"
                )
            }
        ),
    )
    @action(detail=False, methods=['delete'], url_path='delete_backup', name='users-delete-backup')
    def delete_user_backup(self, request):
        username = request.data.get('username')

        if not username:
            return Response({"error": "The 'username' field is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()

        if not user:
            return Response(
                {"error": f"User '{username}' not found in the database."},
                status=status.HTTP_404_NOT_FOUND)

        repositories_deleted, _ = Repository.objects.filter(
            owner=user).delete()
        user.delete()

        return Response(
            {
                "message": f"User '{username}' and {repositories_deleted} "
                           f"repositories deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )