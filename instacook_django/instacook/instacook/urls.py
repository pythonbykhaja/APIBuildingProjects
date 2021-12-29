"""instacook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api_instacook.views import UserAPIView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('api_instacook.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('users/', UserAPIView.as_view(), name='users_create'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='create_token'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
]
