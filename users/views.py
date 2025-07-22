from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from users.forms import SignUpModelForm,SignInModelForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View

User = get_user_model()

# Create your views here.

def is_admin(user):
    # return user.is_authenticated and user.is_staff
    return user.groups.filter(name='Admin').exists()


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')

class SignUpView(View):
    template_name = 'auth/signup.html'

    def get(self, request):
        form = SignUpModelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # wait for activation
            user.save()
            messages.success(request, "Account created successfully! Please check your email for activation link.")
            return redirect('sign-in')
        else:
            messages.error(request, "Please correct the errors below.")
            
        return render(request, self.template_name, {'form': form})



# Customized login view
class CustomLoginView(LoginView):
    form_class = SignInModelForm
    
    def get_success_url(self):
        next_url= self.request.GET.get('next')
        
        return next_url if next_url else super().get_success_url()

# Profile view
class CustomProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name() or user.username
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        return context
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'auth/password_reset.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'auth/password_reset_email.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['host'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password reset link sent to your email.")
        return response


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name = 'auth/password_reset.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password has been reset successfully. You can now sign in.")
        return response
    
class ActivateAccountView(View):
    def get(self, request, user_id, token):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('sign-in')

        if user.is_active:
            messages.info(request, "Account is already activated.")
            return redirect('sign-in')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully! You can now sign in.")
        else:
            messages.error(request, "Invalid activation link.")
        
        return redirect('sign-in')

class AdminDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.view_user' 
    login_url = 'sign-in'
    template_name = 'admin/dashboard.html'

    def get(self, request):
        users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        )

        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'

        return render(request, self.template_name, {'users': users})


class AssignRoleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'
    login_url = 'sign-in'
    template_name = 'admin/assign_role.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = AssignRoleForm()
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove existing roles
            user.groups.add(role)  # Assign new role
            messages.success(request, f"Role changed to {role} for {user.username}.")
            return redirect('admin-dashboard')
        return render(request, self.template_name, {'user': user, 'form': form})

class CreateGroupView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.add_group'
    login_url = 'sign-in'
    template_name = 'admin/create_group.html'

    def get(self, request):
        form = CreateGroupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('create-group')
        else:
            messages.error(request, "Error creating group. Please try again.")
            return render(request, self.template_name, {'form': form})



@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class GroupListView(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()