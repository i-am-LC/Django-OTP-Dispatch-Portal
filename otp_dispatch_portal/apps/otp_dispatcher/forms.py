from django import forms

# Import pycountry for use in choice field
import pycountry
# Import phonenumber to be used in validation submitted number
import phonenumbers

# Import models
from .models import OneTimePasscode
from otp_dispatch_portal.apps.client.models import AuthorisedRepresentative

# Form used to send OTP code to AuthRep
class OneTimePasswordForm(forms.ModelForm):

    class Meta:
        model = OneTimePasscode
        fields = ('__all__')
        exclude = ('otp_val', 'attempts_remaining', 'expire_time',
                   'verified', 'verified_datetime', 'created_by', 'company', 'dest_value')
        widgets = {}

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        # Limit filed to active reps assigned to this client/company
        self.fields['auth_rep'].queryset = AuthorisedRepresentative.objects.filter(company=company, active=True)
        self.fields['auth_rep'].label = 'Authorised Representative'


# Form used to validate previously dispatched OPT.
class OneTimePasscodeVerificationForm(forms.ModelForm):

    class Meta:
        model = OneTimePasscode
        fields = ('otp_val',)
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp_val'].label = 'One time passcode'
        self.fields['otp_val'].required = True

    def clean(self):
        cleaned_data = super().clean()
        if any(self.errors):
            return
