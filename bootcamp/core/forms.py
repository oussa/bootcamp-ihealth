from django import forms
from django.contrib.auth.models import User
import re
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _


class IHealthUser(User):
    tryton_username = models.CharField(_('tryton_username'), max_length=30,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid Tryton username.'), 'invalid')
        ])
    tryton_password = models.CharField(_('tryton_password'), max_length=30, )


class ProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=30,
        required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=30,
        required=False)
    job_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=75,
        required=False)
    url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=50,
        required=False)
    tryton_username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=30,
        required=True)
    tryton_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),
        max_length=30,
        required=True)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'job_title', 'email', 'url', 'location', 'tryton_username', 'tryton_password', ]

    def full_clean(self):
        'Strip whitespace automatically in all form fields'
        data = self.data.copy()
        for k, vs in self.data.lists():
            new_vs = []
            for v in vs:
                new_vs.append(v.strip())
            data.setlist(k, new_vs)
        self.data = data
        super(ProfileForm, self).full_clean()


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="Old password",
        required=True)

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="New password",
        required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(['Old password don\'t match'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class(['Passwords don\'t match'])
        return self.cleaned_data