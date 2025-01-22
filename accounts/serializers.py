from rest_framework import serializers
from . import models
from announcement.serializers import CategorySerializer
from announcement.models import Category
from common.serializers import UserAddressSerializer



class UserForGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'username', 'password', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['address'] = UserAddressSerializer(instance.validate_address).data
        representation['category'] = CategorySerializer(instance.category).data
        return representation


class UserForCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = models.User
        fields = ('id', 'username', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        user.is_active = False
        user.save()
        return user