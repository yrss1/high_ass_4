from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import CustomUserCreationForm, CustomAuthenticationForm, SensitiveDataForm
from .models import CustomUser, SensitiveData
from .serializers import CustomUserSerializer, SensitiveDataSerializer
from .permissions import IsOwnerOrReadOnly
from .throttles import CustomUserRateThrottle


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'secure_app/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_two_factor_enabled:
                device = get_user_totp_device(user)
                if device is None:
                    device = user.totpdevice_set.create(name='Default')
                if device.verify_token(form.cleaned_data['otp_token']):
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error('otp_token', 'Invalid OTP token')
            else:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'secure_app/login.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def setup_2fa(request):
    if request.method == 'POST':
        device = get_user_totp_device(request.user)
        if device is None:
            device = request.user.totpdevice_set.create(name='Default')
        request.user.is_two_factor_enabled = True
        request.user.save()
        return render(request, 'secure_app/setup_2fa_complete.html', {'device': device})
    return render(request, 'secure_app/setup_2fa.html')


def get_user_totp_device(user, name='Default'):
    devices = devices_for_user(user, confirmed=True)
    for device in devices:
        if isinstance(device, TOTPDevice) and device.name == name:
            return device
    return None


@login_required
@require_http_methods(["GET", "POST"])
def sensitive_data(request):
    if request.method == 'POST':
        form = SensitiveDataForm(request.POST)
        if form.is_valid():
            sensitive_data = form.save(commit=False)
            sensitive_data.user = request.user
            sensitive_data.save()
            return redirect('sensitive_data')
    else:
        form = SensitiveDataForm()
    user_data = SensitiveData.objects.filter(user=request.user)
    return render(request, 'secure_app/sensitive_data.html', {'form': form, 'user_data': user_data})


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [CustomUserRateThrottle]

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=400)


class SensitiveDataViewSet(viewsets.ModelViewSet):
    queryset = SensitiveData.objects.all()
    serializer_class = SensitiveDataSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [CustomUserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return SensitiveData.objects.filter(user=self.request.user)
