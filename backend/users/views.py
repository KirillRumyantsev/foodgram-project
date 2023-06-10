from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'actioned':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
