from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django_otp.decorators import otp_required
from .models import UserProfile, SecureData, Email
from .serializers import UserSerializer, UserProfileSerializer, SecureDataSerializer, EmailSerializer
from .forms import EmailForm
from .tasks import send_email_task
from .throttles import CustomUserRateThrottle


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [CustomUserRateThrottle]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class SecureDataViewSet(viewsets.ModelViewSet):
    queryset = SecureData.objects.all()
    serializer_class = SecureDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]

    def get_queryset(self):
        return SecureData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]


@method_decorator(csrf_protect, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


# @login_required
# @otp_required
# @csrf_protect
def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            send_email_task.delay(email.id)
            messages.success(request, 'Email is being sent in the background.')
            return redirect('send_email')
    else:
        form = EmailForm()
    return render(request, 'tasks/send_email.html', {'form': form})
