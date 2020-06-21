from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View





class FtApiSignIn(TemplateView):
	template_name = "account/sign_in.html"
