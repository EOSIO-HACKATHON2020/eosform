from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic import TemplateView
from eos import EOS


class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'eos': EOS()
        })
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request, *args, **kwargs)


def page_400(request):
    return render('400.html', {}, status=400)


def page_403(request):
    return render('403.html', {}, status=403)


def page_404(request):
    return render('404.html', {}, status=404)


def page_500(request):
    return render('500.html', {}, status=500)
