import logging
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import SignupForm


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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'


class SignoutView(LoginRequiredMixin, View):
    """
    Signout the user
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('landing'))
