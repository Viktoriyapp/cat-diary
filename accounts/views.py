from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CatUserRegisterForm


class RegisterView(CreateView):
    form_class = CatUserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
