from django.contrib import admin
from django.urls import path, include
from tasks.views import send_email
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from secure_app import views


router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'sensitive-data', views.SensitiveDataViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', send_email, name='send_email'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('setup-2fa/', views.setup_2fa, name='setup_2fa'),
    path('sensitive-data/', views.sensitive_data, name='sensitive_data'),
]

