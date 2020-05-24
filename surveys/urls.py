from django.urls import path
from . import views


app_name = 'surveys'


urlpatterns = [
    path('create/', views.CreateSurveyView.as_view(), name='create'),
    path('<str:uid>/', views.SurveyView.as_view(), name='survey'),
]
