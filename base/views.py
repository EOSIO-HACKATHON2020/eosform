from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic import TemplateView
from eos import EOS
from surveys.models import Survey
from surveys.models import SurveyStatus


class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_surveys(self):
        return Survey.objects.filter(status=SurveyStatus.PUBLISHED.value)\
                   .order_by('-modified', '-created')[:20]

    def get_context_data(self, **kwargs):
        kwargs.update({
            'eos': EOS(),
            'surveys': self.get_surveys()
        })
        return super().get_context_data(**kwargs)


def page_400(request):
    return render('400.html', {}, status=400)


def page_403(request):
    return render('403.html', {}, status=403)


def page_404(request):
    return render('404.html', {}, status=404)


def page_500(request):
    return render('500.html', {}, status=500)
