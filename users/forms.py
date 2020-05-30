from django import forms
from django.utils.translation import gettext as _
from .models import User


class SignupForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': _('your email here')
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('password')
    }), required=True, label=_('Password'))
    has_accepted_terms = forms.BooleanField(
        label=_('Accept terms of service and privacy policy'))

    class Meta:
        model = User
        fields = [
            # TODO use UsernameField
            'email',
        ]

    def clean_has_accepted_terms(self):
        data = self.cleaned_data.get('has_accepted_terms')
        if not data:
            raise forms.ValidationError(
                _('In order to signup you must accept our terms of service '
                  'and privacy policy'))
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.set_password(self.cleaned_data.get('password'))
            instance.save()

        return instance


# class SigninForm(forms.Form):
#     email = forms.EmailField(required=True, label=_('Email'))
#     password = forms.CharField(required=True, widget=forms.PasswordInput)
#
#     def clean(self):
#         data = super().clean()
#         user = User.objects.filter(email=data.get('email')).first()
#         if user and


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label=_('Email'), required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': _('your email here')
                             }))


class FinishResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('type your password')
    }), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('repeat your password')
    }), required=True)

    def clean(self):
        data = super().clean()
        if data['password'] != data['password_confirm']:
            # TODO what if the password is too weak?
            raise forms.ValidationError(_('Password do not match'))
