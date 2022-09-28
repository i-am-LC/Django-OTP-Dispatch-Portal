from django.db import models

from django.contrib.auth.models import User
from otp_dispatch_portal.apps.client.models import Client, AuthorisedRepresentative

class OneTimePasscode(models.Model):
    REASON_CHOICES = (
        (1, "Cancellation of service/account."),
        (2, "Service block/suspension request."),
        (3, "Adding/Removing a person as a customer's authorised representative."),
        (4, "Disclosure of personal information, "
              "business information or account security information relating to the account."),
        (5, "Additional ongoing or a large one-off charge applied to customers account."),
        (6, "SIM Swap Request."),
        (7, "Transfer service from post-paid to prepaid."),
        (8, "Activation of service request."),
        (9, "Change of ownership of account."),
        (10, "Change customer specific detail - DOB, email, contact details, etc."),
        (11, "Request to block IMEI."),
        (12, "Request to purchase additional mobile device."),
        (13, "Request to add additional service to an account."),
    )
    DESTINATION_CHOICES = (
        ("SMS", "Mobile SMS"),
        ("EML", "Email")
    )

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    auth_rep = models.ForeignKey(AuthorisedRepresentative, on_delete=models.CASCADE)
    destination = models.CharField(max_length=3, choices=DESTINATION_CHOICES)
    # record the true location OTP was sent to.
    dest_value = models.CharField(max_length=254)

    reason = models.IntegerField(choices=REASON_CHOICES)
    # System generated code sent to mobile number.
    otp_val = models.CharField(blank=True, null=True, max_length=6)
    # OTP code provided by SMS recipient.
    attempts_remaining = models.IntegerField(default=3, blank=True, null=True)
    expire_time = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    verified_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.company) + ' ' + str(self.created)