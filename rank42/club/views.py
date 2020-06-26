import random
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy, reverse
from .models import ClubMember, Club
from .forms import ClubForm, ClubMemberForm
from django.contrib.auth.mixins import UserPassesTestMixin


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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["member_list"] = ClubMember.objects.filter(club=self.get_object(), is_join=True)
		if ClubMember.objects.filter(club=self.get_object(), user=self.request.user).exists():
			context["am_i_member"] = 0
		else:
			context["am_i_member"] = 1
		if self.get_object().master == self.request.user:
			context["am_i_master"] = 1
		else:
			context["am_i_member"] = 0
		return context


class ClubJoin(LoginRequiredMixin, CreateView):
	template_name = "club/club_join.html"
	form_class = ClubMemberForm
	success_url = reverse_lazy('club_list')
	pk_url_kwarg = 'club_id'

	def form_valid(self, form):
		form.instance.club = Club.objects.get(id=self.kwargs.get(self.pk_url_kwarg))
		form.instance.user = self.request.user
		return super().form_valid(form)


class ClubManage(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Club
	template_name = "club/club_manage.html"
	context_object_name = 'club'
	pk_url_kwarg = 'club_id'

	def test_func(self):
		if self.get_object().master == self.request.user:
			return True
		else:
			return False

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['waiting'] = ClubMember.objects.filter(club=self.get_object(), is_join=False)
		context['joining'] = ClubMember.objects.filter(club=self.get_object(), is_join=True)
		return context

	def post(self, request, club_id):
		flag = request.POST.get('flag')
		if flag == "delete":
			club_member = ClubMember.objects.get(id=int(request.POST.get('id')))
			club_member.delete()
		elif flag == "join":
			club_member = ClubMember.objects.get(id=int(request.POST.get('id')))
			club_member.is_join = True
			club_member.save()
		return HttpResponseRedirect(reverse('club_manage', kwargs={'club_id': club_id}))


class ClubMyPage(LoginRequiredMixin, ListView):
	context_object_name = 'mypage'
	template_name = "club/club_mypage.html"

	def get_queryset(self):
		queryset = {
			'waiting': ClubMember.objects.filter(user=self.request.user, is_join=False),
			'joining': ClubMember.objects.filter(user=self.request.user, is_join=True),
		}
		return queryset
