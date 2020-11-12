from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView, LogoutView
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserSerializer, UserUpdateSerializer, UserRegisterSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)


class UserLoginAPIView(LoginView):
    pass


class UserLogoutAPIView(LogoutView):
    pass


class UserRegisterAPIView(RegisterView):
    serializer_class = UserRegisterSerializer
