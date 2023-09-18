from django.contrib import admin

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, ResetPasswordView, ChangePasswordView

from users.forms import LoginForm
from django.contrib.auth.views import LoginView,LogoutView

from users import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users.urls')),

    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),


# # admin
path('adminlogin', LoginView.as_view(template_name='admin/adminlogin.html'),name='adminlogin'),
 path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
path('logout', LogoutView.as_view(template_name='admin/adminlogin.html'),name='logout'),
# # customer
# path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
path('admin-customer', views.admin_customer_view,name='admin-customer'),
    path('admin-view-customer',views.admin_view_customer_view,name='admin-view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-add-customer', views.admin_add_customer_view,name='admin-add-customer'),
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),


    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    
    path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),

    path('admin-mechanic', views.admin_mechanic_view,name='admin-mechanic'),
    path('admin-view-mechanic',views.admin_view_mechanic_view,name='admin-view-mechanic'),
    path('delete-mechanic/<int:pk>', views.delete_mechanic_view,name='delete-mechanic'),
    path('update-mechanic/<int:pk>', views.update_mechanic_view,name='update-mechanic'),
    path('admin-add-mechanic',views.admin_add_mechanic_view,name='admin-add-mechanic'),
    path('admin-approve-mechanic',views.admin_approve_mechanic_view,name='admin-approve-mechanic'),
    path('approve-mechanic/<int:pk>', views.approve_mechanic_view,name='approve-mechanic'),
    path('delete-mechanic/<int:pk>', views.delete_mechanic_view,name='delete-mechanic'),
    path('admin-view-mechanic-salary',views.admin_view_mechanic_salary_view,name='admin-view-mechanic-salary'),
    path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),

    path('admin-mechanic-attendance', views.admin_mechanic_attendance_view,name='admin-mechanic-attendance'),
    path('admin-take-attendance', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance', views.admin_view_attendance_view,name='admin-view-attendance'),
    path('admin-feedback', views.admin_feedback_view,name='admin-feedback'),

    path('admin-report', views.admin_report_view,name='admin-report'),


    path('admin-services', views.admin_services_view,name='admin-services'),
    path('admin-category', views.categories,name='admin-category'),
path('logout', LogoutView.as_view(template_name='admin/adminlogin.html'),name='logout'),
    path('mechanic-dashboard/', views.mechanic_dashboard_view,name='mechanic-dashboard'),
    path('mechanic-work-assigned', views.mechanic_work_assigned_view,name='mechanic-work-assigned'),
    path('mechanic-update-status/<int:pk>', views.mechanic_update_status_view,name='mechanic-update-status'),
    path('mechanic-feedback', views.mechanic_feedback_view,name='mechanic-feedback'),
    path('mechanic-salary', views.mechanic_salary_view,name='mechanic-salary'),
    path('mechanic-profile', views.mechanic_profile_view,name='mechanic-profile'),
    path('edit-mechanic-profile', views.edit_mechanic_profile_view,name='edit-mechanic-profile'),

    path('mechanic-attendance', views.mechanic_attendance_view,name='mechanic-attendance'),
    path('mechanicsclick', views.mechanicsclick_view),
path('mechanicsignup', views.mechanic_signup_view,name='mechanicsignup'),
path('mechaniclogin', LoginView.as_view(template_name='Employee/mechaniclogin.html'),name='mechaniclogin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
