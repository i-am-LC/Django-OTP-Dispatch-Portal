from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^otp-verfication/(?P<pk>\d+)/$',
        views.otp_verification_page, name='otp_verification_page'),
]