from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from users.forms import SignUpModelForm,SignInModelForm,AssignRoleForm,CreateGroupForm
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
    
def admin_dashboard(request):
    users= User.objects.all()
    return render(request, 'admin/dashboard.html',{'users': users})
    # if request.user.is_authenticated and request.user.is_staff:
    #     return render(request, 'admin/dashboard.html',{'users': users})
    # else:
    #     messages.error(request, "You do not have permission to access this page.")
    #     return redirect('sign-in')

def assign_role(request, user_id):
    user = User.objects.get(pk=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form= AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Clear existing roles
            user.groups.add(role) # Assign new role
            messages.success(request, f"Role changed to {role} for {user.username}.")
            return redirect('admin-dashboard')
        
    return render(request, 'admin/assign_role.html', {'user': user, 'form': form})

def create_group(request):
    form =CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('create-group')
        else:
            messages.error(request, "Error creating group. Please try again.")

    return render(request, 'admin/create_group.html', {'form': form})

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_list.html', {'groups': groups})