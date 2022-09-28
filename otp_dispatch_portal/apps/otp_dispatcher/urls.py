from django.urls import path

from .views import otp_verification_page

urlpatterns = [
    path('otp-verfication/<pk>/', otp_verification_page, name='otp_verification_page'),
]