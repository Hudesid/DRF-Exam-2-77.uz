from rest_framework import serializers
from . import models


class UserForGetSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'username', 'password', 'product', 'phone_number', 'category', 'address', 'profile_photo')

    def get_category(self, obj):
        from announcement.serializers import CategorySerializer
        return CategorySerializer(obj.category).data

    def get_address(self, obj):
        from common.serializers import UserAddressSerializer
        return UserAddressSerializer(obj.validate_address).data


class UserForCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'username', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def get_category(self, obj):
        from announcement.serializers import CategorySerializer
        return CategorySerializer(obj.category).data


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user