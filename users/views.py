from django.views.generic import TemplateView


class SignupView(TemplateView):
    """
    View to handle signup process
    """
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class SigninView(TemplateView):
    """
    View to handle signin process
    """
    template_name = 'users/signin.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
