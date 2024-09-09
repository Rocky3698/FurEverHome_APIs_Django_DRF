from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer

User= get_user_model()


class CreateUserView(CreateAPIView):
    queryset                = User.objects.all()
    serializer_class        = UserSerializer
    permission_classes      = [AllowAny]