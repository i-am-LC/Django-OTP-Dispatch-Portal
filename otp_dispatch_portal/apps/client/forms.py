from django import forms

# Import pycountry for use in choice field
import pycountry
# Import phonenumber to be used in validation submitted number
import phonenumbers

from .models import Client, AuthorisedRepresentative

class ClientCreateForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('__all__')
        exclude = ('created_by', 'modified_by',)
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if any(self.errors):
            return


class AuthRepCreateForm(forms.ModelForm):
    country = forms.ChoiceField(choices=[])

    class Meta:
        model = AuthorisedRepresentative
        fields = ('__all__')
        exclude = ('created_by', 'modified_by', 'company')
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstname'].label = 'First name'
        self.fields['surname'].label = 'Last name'
        self.fields['email'].label = 'Email'
        self.fields['mobile'].label = 'Mobile'
        self.fields['firstname'].label = 'First name'
        self.fields['surname'].label = 'Last name'
        self.fields['email'].label = 'Email'
        self.fields['mobile'].label = 'Mobile'
        self.fields['country'].choices = \
            sorted([(country.alpha_2, country.name)
                    for country in pycountry.countries],
                   key=lambda x: x[1])

    def clean(self):
        cleaned_data = super().clean()
        if any(self.errors):
            return
        msn = cleaned_data['mobile']
        country = cleaned_data['country']
        # Only accept numeric values (model is char field)
        if msn.isnumeric() == False:
            raise forms.ValidationError(
                "Mobile service number must be numeric.", code='error')
        # Using phonenumbers test validity of provided msn.
        msn_test = phonenumbers.parse(msn, country)
        if phonenumbers.is_possible_number(msn_test) is False \
                or phonenumbers.is_valid_number(msn_test) is False:
            raise forms.ValidationError('Phone number is invalid '
                                        'for the selected country.')


