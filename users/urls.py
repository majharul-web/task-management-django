from django.urls import path
from users.views import CustomLoginView,CustomProfileView,CustomPasswordChangeView,CustomPasswordResetView,CustomPasswordResetConfirmView,EditProfileView,GroupListView,CreateGroupView,AssignRoleView,SignUpView,ActivateAccountView,AdminDashboardView
from django.contrib.auth.views import LogoutView,PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(template_name='auth/signin.html'), name='sign-in'),
    path('profile/', CustomProfileView.as_view(), name='profile'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', LogoutView.as_view() , name='sign-out'),
    # path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/assign-role/<int:user_id>/', AssignRoleView.as_view(), name='assign-role'),
    path('admin/create-group/', CreateGroupView.as_view(), name='create-group'),
    path('admin/group-list/', GroupListView.as_view(), name='group-list'),

    path('password-change/', CustomPasswordChangeView.as_view(template_name="accounts/password_change.html"), name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile')
]