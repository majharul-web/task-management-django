from django.urls import path
from users.views import sign_up, sign_in, sign_out,activate_account, admin_dashboard,assign_role,create_group,group_list,CustomLoginView,CustomProfileView,CustomPasswordChangeView
from django.contrib.auth.views import LogoutView,PasswordChangeView, PasswordChangeDoneView 


urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(template_name='auth/signin.html'), name='sign-in'),
    path('profile/', CustomProfileView.as_view(), name='profile'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', LogoutView.as_view() , name='sign-out'),
    # path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_account, name='activate-account'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/assign-role/<int:user_id>/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    
    path('password-change/', CustomPasswordChangeView.as_view(template_name="accounts/password_change.html"), name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]