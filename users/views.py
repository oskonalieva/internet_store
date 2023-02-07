from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from users.forms import AuthForm, RegisterForm
from django.contrib.auth import authenticate, logout, login
from django.views.generic import CreateView, RedirectView, ListView

# Create your views here.


class AuthView(ListView, CreateView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': AuthForm
        }

    def post(self, request, *args, **kwargs):
        form = AuthForm(data=self.request.POST)

        if form.is_valid():

            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('/products/')
            else:
                form.add_error('username', 'вы что то неправильно ввели')

        return render(request, 'users/auth.html', context={'form': form})


class RegisterView(CreateView):
    def get_context_data(self, **kwargs):

        return {
            'form': RegisterForm,
        }

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=self.request.POST)
        if form.is_valid():
            password1, password2 = form.cleaned_data.get('password1'), form.cleaned_data.get('password2')
            if password1 == password2:
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                return redirect('/products/')
            else:
                form.add_error('password1', 'ошибка')

        return render(request, 'users/register.html', context={
            'form': form,
        })


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/products/')