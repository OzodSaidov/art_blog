from django.shortcuts import render
from django.views.generic import TemplateView

class UserProfileView(TemplateView):
    template_name = 'profile/index.html'


class UserRegisterView(TemplateView):
    template_name = 'register/index.html'



