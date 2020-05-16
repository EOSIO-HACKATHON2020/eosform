from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]