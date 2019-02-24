from django.http import HttpResponseRedirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('login/')),
    path('login/', views.ShowLoginForm.as_view()),
    path('registration/', views.ShowRegistrationForm.as_view()),
    path('message/', views.ShowSendMessageForm.as_view()),
    path('logout/', views.logout)
]