import logging
from typing import Union
from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404
from . import forms
from .models import Survey
from .models import Question


logger = logging.getLogger(__name__)


class CreateSurveyView(LoginRequiredMixin, TemplateView):
    template_name = 'surveys/create.html'
    form_class = forms.SurveyForm

    def get_form(self):
        return self.form_class(data=self.request.POST or None,
                               user=self.request.user, prefix='s')

    def get_formset(self):
        return forms.QuestionFormSet(self.request.POST or None, prefix='q')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.get_form(),
            'formset': self.get_formset(),
        })
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset()

        if form.is_valid() and formset.is_valid():
            survey = form.save()

            for question_form in formset.forms:
                q: Question = question_form.save()
                q.survey = survey
                q.save()
            return HttpResponseRedirect(survey.get_absolute_url())

        ctx = self.get_context_data(**kwargs)
        ctx.update({
            'form': form,
            'formset': formset,
        })
        return self.render_to_response(ctx)


class SurveyView(LoginRequiredMixin, TemplateView):
    template_name = 'surveys/survey.html'

    def get_object(self):
        uid = self.kwargs.get('uid')
        return Survey.objects.filter(user=self.request.user).filter(uid=uid)\
            .first()

    def get_queryset(self):
        return Survey.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'survey': self.get_object()
        })
        return super().get_context_data(**kwargs)


class SurveyActionView(LoginRequiredMixin, View):

    def get_object(self) -> Union[None, Survey]:
        uid = self.kwargs.get('uid')
        return Survey.objects.filter(uid=uid, user=self.request.user).first()

    def get(self, request, *args, **kwargs):
        survey = self.get_object()
        if not survey:
            raise Http404()

        action = kwargs.get('action')
        if action not in ['publish', 'deactivate']:
            raise Http404()

        if survey.is_draft and action == 'publish':
            data = survey.publish()
        elif survey.is_published and action == 'deactivate':
            data = survey.deactivate()
        else:
            raise PermissionDenied()

        # TODO message
        logger.info(f'Survey {survey.uid} action {action}: {data}')

        return HttpResponseRedirect(survey.get_absolute_url())
