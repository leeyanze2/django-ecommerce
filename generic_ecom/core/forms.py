from django import forms
from django.utils.translation import ugettext_lazy as _


class FormLogin(forms.Form):
    """
    THE LOGIN FORM DOCUMENTATION
    """
    username = forms.CharField(
        label=_('User Name'),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}))
    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}))
