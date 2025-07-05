from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import SignUpModelForm,SignInModelForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator

# Create your views here.


def sign_up(request):
    form = SignUpModelForm()
    if request.method == 'POST':
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False 
            user.save()
            messages.success(request, "Account created successfully! Please check your email for activation link.")
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'auth/signup.html', {"form": form})


def sign_in(request):
    form=SignInModelForm()
    if request.method == 'POST':
        form = SignInModelForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print("Invalid credentials")

    return render(request, 'auth/signin.html', {"form": form})


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')

def activate_account(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
        if user.is_active:
            messages.info(request, "Account is already activated.")
            return redirect('sign-in')
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully! You can now sign in.")
            return redirect('sign-in')
        else:
            messages.error(request, "Invalid activation link.")
            return redirect('sign-in')
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('sign-in')