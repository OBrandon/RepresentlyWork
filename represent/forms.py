from django import forms
from django.core.validators import RegexValidator

class SubmitZipCode(forms.Form):
	zipcode = forms.CharField(max_length=5, min_length=5, label = 'ZipCode', validators=[RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Username must be Alphanumeric',
            code='invalid_username'
        ),
    ])