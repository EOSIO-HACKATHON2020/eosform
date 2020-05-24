from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from . import forms
from .models import Survey


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

        if form.is_valid():
            survey = form.save()
            return HttpResponseRedirect(survey.get_absolute_url())

        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
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
