from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),

    path('reset-pass/', views.ResetPasswordView.as_view(), name='reset-pass'),
    path('reset-pass/finish/<int:id>/<str:code>/',
         views.FinishResetPasswordView.as_view(), name='reset-pass-finish'),
    path('confirm-signup/<int:pk>/<str:code>/',
         views.ConfirmSignupView.as_view(), name='confirm-signup'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('responses/', views.ResponsesView.as_view(), name='responses'),
]
