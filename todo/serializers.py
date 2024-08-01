from rest_framework import serializers
from .models import Task, TaskPermission, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_staff',]


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                           required=False)  # выводим username вместо id
    can_read = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'viewers': {'write_only': True}  # Делаем поле viewers доступным только для записи
        }


class TaskPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPermission
        fields = ['task', 'user', 'can_read', ]
