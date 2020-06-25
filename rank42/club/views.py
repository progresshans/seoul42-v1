import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse_lazy, reverse
from .models import ClubMember, Club
from .forms import ClubForm


class ClubList(LoginRequiredMixin, ListView):
    queryset = random.shuffle(Club.objects.all())
    context_object_name = "clubs"
    paginate_by = 20
    template_name = "club/club_list.html"


class ClubAdd(LoginRequiredMixin, CreateView):
    template_name = "club/club_add.html"
    form_class = ClubForm
    success_url = reverse_lazy('club_list')

    def form_valid(self, form):
        form.instance.master = self.request.user
        return super().form_valid(form)