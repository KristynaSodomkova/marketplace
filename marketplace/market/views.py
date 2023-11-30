from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserLoginForm


class RegisterUserView(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register_user.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The registration was successfull.')
            return redirect('home')
        return render(request, 'register_user.html', {'form': form})


class LoginUserView(View):

    def get(self, request):
        form = CustomUserLoginForm()
        return render(request, 'login_user.html', {'form': form})

    def post(self, request):
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, 'login_user.html', {'form': form})


class HomePageView(View):

    def get(self, request):
        return render(request, "home.html")
