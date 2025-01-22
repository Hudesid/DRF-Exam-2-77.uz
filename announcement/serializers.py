from rest_framework import serializers
from . import models


class ChildrenCategorySerializer(serializers.ModelSerializer):
    ads_count = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ads_count', 'children')

    def get_ads_count(self, obj):
        return obj.ads_count()

    def get_children(self, obj):
        if obj.children.exists():
            return ChildrenCategorySerializer(obj.children, many=True).data
        return []

class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)
    ads_count = serializers.SerializerMethodField()
    children = ChildrenCategorySerializer(read_only=True, many=True)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ads_count', 'icon', 'children')

    def to_representation(self, instance):
        if instance.parent:
            return None
        representation = super().to_representation(instance)
        return representation

    def get_ads_count(self, obj):
        return obj.ads_count()


class ParentCategorySerializer(serializers.ModelSerializer):
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ["id", "name", "ads_count", "icon"]

    def get_ads_count(self, obj):
        return obj.ads_count()


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ["id", "name", "category"]

    def get_category(self, obj):
        if obj.parent.exists():
            return ParentCategorySerializer(read_only=True, many=True)
        return None

class ProductForGetSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)
    sub_category = SubCategorySerializer(source='category', read_only=True)
    address  = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'slug', 'sub_category', 'image', 'price', 'currency', 'published_at', 'updated_at', 'description', 'phone_number', 'address', 'seller', 'extra')


    def get_seller(self, obj):
        from accounts.serializers import UserForGetSerializer
        return UserForGetSerializer(obj.seller).data


    def get_address(self, obj):
        from common.serializers import AddressSerializer
        return AddressSerializer(obj.validate_address).data


    def to_representation(self, instance):
        if not instance.extra:
            return []
        representation = super().to_representation(instance)
        return representation


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)
    sub_category = SubCategorySerializer(source='category', read_only=True)

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'slug', 'sub_category', 'image', 'price', 'currency', 'published_at', 'updated_at', 'description', 'phone_number', 'address', 'seller', 'extra')

    def get_seller(self, obj):
        from accounts.serializers import UserForGetSerializer
        return UserForGetSerializer(obj.seller).data


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PopularSearchWord
        fields = ('id', 'word', 'count')