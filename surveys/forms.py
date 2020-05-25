import requests
from django import forms
from django.utils.translation import gettext as _
from django.forms import modelformset_factory
from config.models import Settings
from .models import Survey
from .models import Question


class SurveyForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True)

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
        # 'type',
        # 'is_required',
    ),
    extra=0,
    max_num=100
)


class ResponseForm(forms.Form):

    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._survey = survey

        for question in self._survey.questions.all():
            field_name = f'field_{question.id}'
            self.fields[field_name] = forms.CharField(
                label=question.name, required=True,
                help_text=question.description)

    def send_to_eos(self):
        settings = Settings.get_solo()
        uri = f'{settings.eosgate}/response'
        payload = {
            'form': self._survey.uid,
            'answers': list(self.cleaned_data.values())
        }
        r = requests.post(uri, json=payload)
        return r.content
