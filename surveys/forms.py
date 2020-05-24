from django import forms
from .models import Survey


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = [
            'name',
            # 'uid',
        ]

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self._user

        if commit:
            instance.save()

        return instance
