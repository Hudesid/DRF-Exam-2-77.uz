from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('accounts/seller/registration/', views.UserCreateAPIView.as_view(), name='register'),
    path('accounts/login/', TokenObtainPairView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('accounts/refresh/', TokenRefreshView.as_view(), name='refresh_login'),
    path('accounts/me/<uuid:id>/', views.UserRetrieveAPIView.as_view(), name='user_detail'),
    path('accounts/me/update/<uuid:id>', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('accounts/me/destroy/<uuid:id>', views.UserDestroyAPIView.as_view(), name='user_delete')
]