from django import forms

# Import pycountry for use in choice field
import pycountry
# Import phonenumber to be used in validation submitted number
import phonenumbers

# Import models
from .models import OneTimePasscodeSMS

# Form used to request OTP dispatch.
class OneTimePasscodeSMSForm(forms.ModelForm):
    country = forms.ChoiceField(choices=[])

    class Meta:
        model = OneTimePasscodeSMS
        fields = ('__all__')
        exclude = ('otp_dispatched_val', 'otp_confirmed_val',
                   'attempts_remaining', 'expire_time', 'verified', 'created_by')
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skip_verification'].label = 'Skip verification'
        self.fields['skip_reason'].label = 'Notes'
        # Set ordered (by country name) pycountry as choice options. Storing the two char country code.
        self.fields['country'].choices = sorted([(country.alpha_2, country.name)
                                                  for country in pycountry.countries],
                                                 key=lambda x: x[1])

    def clean(self):
        cleaned_data = super().clean()
        if any(self.errors):
            return
        msn = cleaned_data['mobile_number']
        country = cleaned_data['country']
        skip_verification = cleaned_data['skip_verification']
        skip_reason = cleaned_data['skip_reason']
        # Only accept numeric values (model is char field)
        if msn.isnumeric() == False:
            raise forms.ValidationError(
                "Mobile service number must be numeric.", code='error')
        # Require notes / skip reason content should skip verification be selected.
        if skip_verification == True:
            if not skip_reason:
                raise forms.ValidationError(
                "Please provide notes detailing the reason for skipping validation and the authorised rep details."
                )
        # Using phonenumbers test validity of provided msn.
        number_test = phonenumbers.parse(msn, country)
        if phonenumbers.is_possible_number(number_test) is False \
                or phonenumbers.is_valid_number(number_test) is False:
            raise forms.ValidationError('Invalid phone number for country.')

# Form used to validate previously dispatched OPT.
class OneTimePasscodeVerificationForm(forms.ModelForm):

    class Meta:
        model = OneTimePasscodeSMS
        fields = ('otp_confirmed_val',)
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp_confirmed_val'].label = 'One time passcode'
        self.fields['otp_confirmed_val'].required = True

    def clean(self):
        cleaned_data = super().clean()
        if any(self.errors):
            return
