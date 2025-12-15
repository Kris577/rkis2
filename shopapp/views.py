from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from .forms import RegisterForm, UpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Choice, CustomUser
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.utils import timezone
from django.views import View
from .forms import QuestionForm, ChoiceFormSet

class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('polls:login')

class Profile(generic.DetailView):
    model = CustomUser
    template_name = 'polls/profile.html'

class DeleteUser(generic.DeleteView):
    model = CustomUser
    template_name = 'polls/user_confirm_delete.html'
    success_url = reverse_lazy('polls:index')

def logout_user(request):
    logout(request)
    return redirect('polls:index')

class UpdateUser(generic.UpdateView):
    model = CustomUser
    form_class = UpdateForm
    template_name = 'polls/user_form.html'
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other_user = CustomUser.objects.get(pk=self.kwargs['pk'])
        if self.request.user.pk != other_user.pk:
            raise Http404

        return context