from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers, models


class AuthorValidateAPIView(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class UserCreateAPIView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserForCreateUpdateSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserForCreateUpdateSerializer
    permission_classes = [AuthorValidateAPIView]


class UserDestroyAPIView(DestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserForGetSerializer
    permission_classes = [AuthorValidateAPIView]


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserForGetSerializer
    lookup_field = 'id'


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail':'Successfully logged out.'})
        except KeyError:
            return Response({'detail':'Refresh token required.'})


class CustomTokenObtainPairView(CreateAPIView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Response(data, status=200)