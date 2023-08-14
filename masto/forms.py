from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class MastodonAccountForm(forms.Form):
    username = forms.CharField(max_length=100)
    access_token = forms.CharField(widget=forms.Textarea)

    helper = FormHelper()
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Save'))
