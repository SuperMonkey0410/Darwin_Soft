from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskPermissionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'task-permissions', TaskPermissionViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    #path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    #path('register/', CreateUserView.as_view(), name='register'),
]
