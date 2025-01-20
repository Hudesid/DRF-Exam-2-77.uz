from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('accounts/seller/registration/', views.UserCreateAPIView.as_view(), name='register'),
    path('accounts/login/', TokenObtainPairView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('accounts/refresh/', TokenRefreshView.as_view(), name='refresh_login'),
    path('accounts/me/', views.UserRetrieveAPIView.as_view(), name='user_detail'),
    path('accounts/me/update/<int:pk>', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('accounts/me/destroy/<int:pk>', views.UserDestroyAPIView.as_view(), name='user_delete'),
    path('store/categories/with/children/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('store/search/complete/', views.SearchAPIView.as_view(), name='search'),
    path('store/ads/create/', views.ProductCreateAPIView.as_view(), name='product_create'),
    path('store/ads/list/', views.ProductListAPIView.as_view(), name='product_list'),
    path('store/ads/update/<slug:slug>/', views.ProductUpdateAPIView.as_view(), name='product_update'),
    path('store/ads/<slug:slug>/', views.ProductRetrieveAPIView.as_view(), name='product_detail'),
    path('store/ads/destroy/<slug:slug>/', views.ProductDestroyAPIView.as_view(), name='product_delete')
]
