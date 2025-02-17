from django.urls import path
from . import views


app_name = 'surveys'


urlpatterns = [
    path('<str:uid>/response/', views.ResponseView.as_view(), name='response'),
    path('create/', views.CreateSurveyView.as_view(), name='create'),
    path('<str:uid>/', views.SurveyView.as_view(), name='survey'),
    path('<str:uid>/json/', views.SurveyView.as_view(
        template_name='surveys/json.html'), name='json'),
    path('<str:uid>/<str:action>/', views.SurveyActionView.as_view(),
         name='action'),
]
