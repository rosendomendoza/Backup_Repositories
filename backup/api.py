from rest_framework.routers import DefaultRouter
from .views.user_views import UserViewSet
from .views.repository_views import RepositoryViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'repositories', RepositoryViewSet, basename='repositories')
