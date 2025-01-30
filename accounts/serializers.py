from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from announcement.models import Category
from common.serializers import AddressSerializer



class UserForGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('guid', 'username', 'password', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['address'] = AddressSerializer(instance.validate_address).data
        from announcement.serializers import CategorySerializer
        representation['category'] = CategorySerializer(instance.category).data
        return representation


class UserForCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    username = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = models.User
        fields = ('guid', 'username', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        user.is_active = False
        user.save()
        return user


User = get_user_model()

class CustomTokenObtainPairSerializer(serializers.Serializer):
    guid = serializers.UUIDField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    def validate(self, validated_data):
        guid = validated_data['guid']
        password = validated_data['password']
        username = validated_data['username']

        try:
            user = User.objects.get(guid=guid, username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid GUID or username or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid GUID or username or password")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }