from django.contrib import admin
from django.urls import path, include
from tasks.views import send_email
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', send_email, name='send_email'),
]

