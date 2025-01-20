from django.db.models import Q
from django.views.generic import ListView
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers, models, paginations


class AuthorValidateAPIView(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj

class AuthorValidateProductAPIView(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.seller


class BaseCategoryAPIView(APIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class BasePrivacyPoliceAPIView(APIView):
    queryset = models.PrivacyPolicy.objects.all()
    serializer_class = serializers.PrivacyPoliceSerializer


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
    permission_classes = [IsAuthenticated]


class CategoryCreateAPIView(BaseCategoryAPIView, CreateAPIView):
    permission_classes = [IsAdminUser]


class CategoryUpdateAPIView(BaseCategoryAPIView, UpdateAPIView):
    permission_classes = [IsAdminUser]


class CategoryDestroyAPIView(BaseCategoryAPIView, DestroyAPIView):
    permission_classes = [IsAdminUser]


class CategoryListAPIView(BaseCategoryAPIView, ListView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['^name', '=parent']


class PrivacyPoliceRetrieveAPIView(BasePrivacyPoliceAPIView, RetrieveAPIView):
    """Privacy Police detail"""


class PrivacyPoliceCreateAPIView(BasePrivacyPoliceAPIView, CreateAPIView):
    permission_classes = [IsAdminUser]


class PrivacyPoliceUpdateAPIView(BasePrivacyPoliceAPIView, UpdateAPIView):
    permission_classes = [IsAdminUser]


class PrivacyPoliceDestroyAPIView(BasePrivacyPoliceAPIView, DestroyAPIView):
    permission_classes = [IsAdminUser]


class ProductListAPIView(ListView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductForGetSerializer
    pagination_class = paginations.ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'price', 'address', 'category', 'published_at']
    filterset_fields = ['price', 'address', 'published_at', 'category', 'currency']
    ordering_fields = ['category']
    ordering = ['category']


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductForGetSerializer

class ProductCreateAPIView(CreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductUpdateAPIView(UpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [AuthorValidateProductAPIView]


class ProductDestroyAPIView(DestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductForGetSerializer
    permission_classes = [AuthorValidateProductAPIView]


class SearchAPIView(APIView):
    queryset = models.Product.objects.all()

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)

        if search_query is None:
            posts = self.queryset
        else:
            search_filter = Q(
                name__icontains=search_query
            ) | Q(
                price__icontains=search_query
            ) | Q(
                currency__icontains=search_query
            ) | Q(
                published_at__icontains=search_query
            ) | Q(
                category__name__icontains=search_query
            ) | Q(
                category__parent__name__icontains=search_query
            ) | Q(
                category__parent__parent__name__icontains=search_query
            )

            posts = self.queryset.filter(search_filter)

        serializer = serializers.ProductSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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