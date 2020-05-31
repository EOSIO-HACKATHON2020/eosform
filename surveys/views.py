import logging
from typing import Union
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404
from . import forms
from .models import SurveyStatus
from .models import Survey
from .models import Question
from .models import Participation


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

            messages.info(request,
                          _(f'Survey {survey.uid} created successfully'))
            return HttpResponseRedirect(survey.get_absolute_url())

        logger.info(formset.errors)
        ctx = self.get_context_data(**kwargs)
        ctx.update({
            'form': form,
            'formset': formset,
        })
        return self.render_to_response(ctx)


class SurveyView(TemplateView):
    template_name = 'surveys/survey.html'

    def get_object(self) -> Union[None, Survey]:
        uid = self.kwargs.get('uid')
        survey = Survey.objects.filter(uid=uid).first()
        user = self.request.user

        if survey:
            if survey.is_published or survey.is_draft and survey.user == user:
                return survey
        return None

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
        if action not in ['publish', 'delete']:
            raise Http404()

        if survey.is_draft and action == 'publish':
            message = survey.eos_publish()
        elif survey.is_published and action == 'delete':
            message = survey.eos_delete()
            survey.delete()
            logger.info(f'Deleted survey {survey.uid}')
        else:
            raise PermissionDenied()

        messages.info(request, message)
        logger.info(f'Survey {survey.uid} action {action}: {message}')

        return HttpResponseRedirect(survey.get_absolute_url())


class ResponseView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "surveys/response.html"
    form_class = forms.ResponseForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = None

    def test_func(self) -> bool:
        if self.request.user.is_anonymous:
            return False

        if self.request.user.is_authenticated and \
                not self.request.user.is_email_verified:
            logger.info(_(f'You must verify your email first'))
            return False

        has_participated = Participation.objects.filter(
            user=self.request.user, survey=self.survey).exists()

        if has_participated:
            messages.warning(self.request,
                             _('You have already participated in this survey'))
            return False
        return True

    def get_object(self):
        params = {
            'uid': self.kwargs.get('uid'),
            'status': SurveyStatus.PUBLISHED.value
        }
        return Survey.objects.filter(**params).first()

    def dispatch(self, request, *args, **kwargs):
        self.survey = self.get_object()

        if not self.survey:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        return self.form_class(data=self.request.POST or None,
                               survey=self.survey, user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.get_form()
        })
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            message = form.send_to_eos()
            messages.info(request, _(f'Response submitted: {message}'))
            return HttpResponseRedirect(self.survey.get_absolute_url())

        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)
