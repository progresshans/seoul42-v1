import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy, reverse
from .models import ClubMember, Club
from .forms import ClubForm, ClubMemberForm


class ClubList(LoginRequiredMixin, ListView):
	queryset = Club.objects.all()
	context_object_name = "clubs"
	paginate_by = 30
	template_name = "club/club_list.html"


class ClubAdd(LoginRequiredMixin, CreateView):
	template_name = "club/club_add.html"
	form_class = ClubForm
	success_url = reverse_lazy('club_list')

	def form_valid(self, form):
		form.instance.master = self.request.user
		return super().form_valid(form)


class ClubDetail(LoginRequiredMixin, DetailView):
	model = Club
	context_object_name = "club"
	template_name = "club/club_detail.html"
	pk_url_kwarg = 'club_id'


class ClubJoin(LoginRequiredMixin, CreateView):
	template_name = "club/club_join.html"
	form_class = ClubMemberForm
	success_url = reverse_lazy('club_list')
	pk_url_kwarg = 'club_id'

	def form_valid(self, form):
		form.instance.club = Club.objects.get(id=self.kwargs.get(self.pk_url_kwarg))
		form.instance.user = self.request.user
		return super().form_valid(form)


class ClubManage()
