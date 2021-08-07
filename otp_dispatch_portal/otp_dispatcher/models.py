from django.db import models


# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
class OneTimePasscodeSMS(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    modified = models.DateTimeField(auto_now=True)
    # Number OTP will be SMS'ed to.
    mobile_number = models.CharField(max_length=12)
    country = models.CharField(max_length=2)
    skip_verification = models.BooleanField(default=False)
    skip_reason = models.TextField(blank=True, null=True)
    # System generated code sent to mobile number.
    otp_dispatched_val = models.CharField(blank=True, null=True, max_length=6)
    # OTP code provided by SMS recipient.
    otp_confirmed_val = models.CharField(blank=True, null=True, max_length=6)
    attempts_remaining = models.IntegerField(default=3, blank=True, null=True)
    expire_time = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(blank=True, null=True)
    verified_datetime = models.DateTimeField(blank=True, null=True)