from django import forms
from django.forms import modelformset_factory
from .models import Survey
from .models import Question


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


QuestionFormSet = modelformset_factory(
    Question, fields=(
        'name',
        'description',
        'type',
        'is_required',
    ),
    extra=0,
    max_num=100
)
