from rest_framework import serializers
from . import models
from announcement.serializers import CategorySerializer


class UserForGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    address = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'username', 'password', 'product', 'phone_number', 'category', 'address', 'profile_photo')

    def get_address(self, obj):
        return obj.validate_address()


class UserForCreateUpdateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = models.User
        fields = ('id', 'username', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user