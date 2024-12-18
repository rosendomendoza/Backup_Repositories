from django.urls import path, include
from .api import router  

urlpatterns = [
    path('api/', include(router.urls)),
]
