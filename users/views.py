import logging
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .otp import OTP
from .models import User
from .forms import SignupForm
from . import forms
from surveys.models import Survey
from surveys.models import SurveyStatus
from surveys.models import Participation


logger = logging.getLogger(__name__)


class SignupView(TemplateView):
    """
    View to handle signup process
    """
    template_name = 'users/signup.html'
    form_class = SignupForm

    def get_form(self):
        return self.form_class(data=self.request.POST or None)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.get_form()
        })
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user.request_confirm_email()
            # TODO add message about success
            logger.info(f'User {user.id} "{user.email}" signed up')
            return HttpResponseRedirect(reverse('users:dashboard'))
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


class SigninView(LoginView):
    """
    View to handle signin process
    """
    template_name = 'users/signin.html'
    next = reverse_lazy('users:dashboard')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class DashboardView(TemplateView):
    template_name = 'users/dashboard.html'

    @staticmethod
    def get_anonymous_surveys():
        return Survey.objects.filter(Q(status=SurveyStatus.PUBLISHED.value))

    def get_authenticated_surveys(self):
        return Survey.objects.filter(
            Q(user=self.request.user) |
            Q(status=SurveyStatus.PUBLISHED.value))

    def get_surveys(self):
        if self.request.user.is_authenticated:
            return self.get_authenticated_surveys()
        return self.get_anonymous_surveys()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'surveys': self.get_surveys()
        })
        return super().get_context_data(**kwargs)


class ResponsesView(TemplateView):
    template_name = 'users/responses.html'

    @staticmethod
    def get_anonymous_surveys():
        return Survey.objects.filter(Q(status=SurveyStatus.PUBLISHED.value))

    def get_authenticated_surveys(self):
        pks = self.request.user.surveys_participated\
            .values_list('id', flat=True)
        return Survey.objects.filter(
            Q(user=self.request.user) |
            Q(status=SurveyStatus.PUBLISHED.value)
        ).exclude(pk__in=pks)

    def get_surveys(self):
        if self.request.user.is_authenticated:
            return self.get_authenticated_surveys()
        return self.get_anonymous_surveys()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'surveys': self.get_surveys()
        })
        return super().get_context_data(**kwargs)


class SignoutView(LoginRequiredMixin, View):
    """
    Signout the user
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('landing'))


class ConfirmSignupView(View):
    """
    Confirm signup
    """
    def get(self, request, *args, **kwargs):
        user = self.get_user()
        otp = OTP('confirm_signup', user.id)
        code = self.kwargs.get('code')
        if otp.code != code:
            raise PermissionDenied
        else:
            user.is_email_verified = True
            user.save()
            # TODO logger
            # TODO message
        return HttpResponseRedirect(reverse('users:signin'))

    def get_user(self) -> User:
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)


class FinishResetPasswordView(TemplateView):
    template_name = 'users/finish_reset_password.html'
    form_class = forms.FinishResetPasswordForm

    def get_form(self):
        return self.form_class(data=self.request.POST or None)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.get_form()
        })
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        user = self.get_user()
        code = self.kwargs.get('code')
        otp = OTP('reset_password', user.id)
        if otp.code != code:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_user(self) -> User:
        user_id = self.kwargs.get('id')
        return get_object_or_404(User, pk=user_id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = self.get_user()
            user.set_password(form.cleaned_data['password'])
            user.save()
            # TODO logger password changed
            # TODO message
            return HttpResponseRedirect(reverse('users:dashboard'))
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


class ResetPasswordView(TemplateView):
    template_name = 'users/reset_password.html'
    form_class = forms.ResetPasswordForm

    def get_form(self):
        return self.form_class(data=self.request.POST or None)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.get_form()
        })
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                user.reset_password()
                # TODO logger
                logger.info('password reset initiated')
                # TODO message
            return HttpResponseRedirect(reverse('users:signin'))
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)
