from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


from .models import profile

# Add google play API


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        temp = request.POST.get('email')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'sign-up.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'sign-up.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['passwrd']
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'sign-in.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'sign-in.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/')


@login_required
def dashboard(request):
    pass


@login_required
def ride(request):
    pass
