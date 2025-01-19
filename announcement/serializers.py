from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)
    ads_count = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'icon', 'children')

    def get_count(self, obj):
        return obj.count()

    def get_children(self, instance):
        return models.Category.objects._build_tree(instance)


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
        fields = ('id', 'username', 'password', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class ParentCategorySerializer(serializers.ModelSerializer):
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ["id", "name", "ads_count", "icon"]

    def get_ads_count(self, obj):
        return obj.ads_count()


class SubCategorySerializer(serializers.ModelSerializer):
    category = ParentCategorySerializer(source="parent", read_only=True)

    class Meta:
        model = models.Category
        fields = ["id", "name", "category"]


class ProductForGetSerializer(serializers.ModelSerializer):
    seller = UserForGetSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    sub_category = SubCategorySerializer(source='category', read_only=True)
    address  = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'slug', 'sub_category', 'image', 'price', 'currency', 'published_at', 'updated_at', 'description', 'phone_number', 'address', 'seller', 'extra')

    def validate_address(self, obj):
        return obj.validate_address()

    def to_representation(self, instance):
        if not instance.extra:
            return []
        representation = super().to_representation(instance)
        return representation


class ProductSerializer(serializers.ModelSerializer):
    seller = UserForGetSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    sub_category = SubCategorySerializer(source='category', read_only=True)

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'slug', 'sub_category', 'image', 'price', 'currency', 'published_at', 'updated_at', 'description', 'phone_number', 'address', 'seller', 'extra')


class PrivacyPoliceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrivacyPolicy
        fields = ('id', 'created_at', 'updated_at', 'description')