from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required,user_passes_test

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from . import forms,models
from django.db.models import Q

from django.http import HttpResponseRedirect
from django.db.models import Sum
# from users.forms import CustomerForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from users.models import Request,Category
from .forms import CategoryForm
from django.views.generic.edit import CreateView

def index(request):
    return render(request,'users/index.html')
def home(request):
    return render(request, 'users/home.html')
def about(request):
    return render(request,'users/about.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
            success_url = reverse_lazy('users-home')

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


# admin


def is_mechanic(user):
    return user.groups.filter(name='MECHANIC').exists()


def afterlogin_view(request):
    if is_mechanic(request.user):
        accountapproval=models.Mechanic.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('mechanic-dashboard')
        else:
            return render(request,'Employee/mechanic_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.User.objects.filter(is_superuser=False).count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'admin/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'admin/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    user=User.objects.filter(is_superuser=False)
    mechanic=User.objects.filter(mechanic=False)
    context = {
         'customers' : customers,
         'user' : user,
         'mechanic':mechanic
     }
    return render(request,'admin/admin_view_customer.html',context)


@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'admin/update_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'admin/admin_add_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'admin/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'admin/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_mechanic_view(request):
    return render(request,'admin/admin_mechanic.html')


@login_required(login_url='adminlogin')
def admin_approve_mechanic_view(request):
    mechanics=models.Mechanic.objects.all().filter(status=False)
    return render(request,'admin/admin_approve_mechanic.html',{'mechanics':mechanics})

@login_required(login_url='adminlogin')
def approve_mechanic_view(request,pk):
    mechanicSalary=forms.MechanicSalaryForm()
    if request.method=='POST':
        mechanicSalary=forms.MechanicSalaryForm(request.POST)
        if mechanicSalary.is_valid():
            mechanic=models.Mechanic.objects.get(id=pk)
            mechanic.salary=mechanicSalary.cleaned_data['salary']
            mechanic.status=True
            mechanic.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-mechanic')
    return render(request,'admin/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})


@login_required(login_url='adminlogin')
def delete_mechanic_view(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('admin-approve-mechanic')


@login_required(login_url='adminlogin')
def admin_add_mechanic_view(request):
    userForm=forms.MechanicUserForm()
    mechanicForm=forms.MechanicForm()
    mechanicSalary=forms.MechanicSalaryForm()
    mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanicSalary':mechanicSalary}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES)
        mechanicSalary=forms.MechanicSalaryForm(request.POST)
        if userForm.is_valid() and mechanicForm.is_valid() and mechanicSalary.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanic=mechanicForm.save(commit=False)
            mechanic.user=user
            mechanic.status=True
            mechanic.salary=mechanicSalary.cleaned_data['salary']
            mechanic.save()
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-mechanic')
        else:
            print('problem in form')
    return render(request,'admin/admin_add_mechanic.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_mechanic_view(request):
    mechanics=models.Mechanic.objects.all()
    return render(request,'admin/admin_view_mechanic.html',{'mechanics':mechanics})


@login_required(login_url='adminlogin')
def delete_mechanic_view(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('admin-view-mechanic')


@login_required(login_url='adminlogin')
def update_mechanic_view(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    userForm=forms.MechanicUserForm(instance=user)
    mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
    mydict={'userForm':userForm,'mechanicForm':mechanicForm}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST,instance=user)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('admin-view-mechanic')
    return render(request,'admin/update_mechanic.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_mechanic_salary_view(request):
    mechanics=models.Mechanic.objects.all()
    return render(request,'admine/admin_view_mechanic_salary.html',{'mechanics':mechanics})

@login_required(login_url='adminlogin')
def update_salary_view(request,pk):
    mechanicSalary=forms.MechanicSalaryForm()
    if request.method=='POST':
        mechanicSalary=forms.MechanicSalaryForm(request.POST)
        if mechanicSalary.is_valid():
            mechanic=models.Mechanic.objects.get(id=pk)
            mechanic.salary=mechanicSalary.cleaned_data['salary']
            mechanic.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-mechanic-salary')
    return render(request,'admin/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'admin/admin_request.html')

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'admin/admin_view_request.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'admin/admin_approve_request_details.html',{'adminenquiry':adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')



@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry=forms.RequestForm()
    adminenquiry=forms.AdminRequestForm()
    mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        adminenquiry=forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=adminenquiry.cleaned_data['customer']
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status='Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request,'admin/admin_add_request.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'admin/admin_approve_request.html',{'enquiry':enquiry})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'admin/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'admin/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request,'admin/update_cost.html',{'updateCostForm':updateCostForm})



@login_required(login_url='adminlogin')
def admin_mechanic_attendance_view(request):
    return render(request,'admin/admin_mechanic_attendance.html')


@login_required(login_url='adminlogin')
def admin_take_attendance_view(request):
    mechanics=models.Mechanic.objects.all().filter(status=True)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                print(mechanics[i].id)
                print(int(mechanics[i].id))
                mechanic=models.Mechanic.objects.get(id=int(mechanics[i].id))
                AttendanceModel.mechanic=mechanic
                AttendanceModel.save()
            return redirect('admin-view-attendance')
        else:
            print('form invalid')
    return render(request,'admin/admin_take_attendance.html',{'mechanics':mechanics,'aform':aform})

@login_required(login_url='adminlogin')
def admin_view_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date)
            mechanicdata=models.Mechanic.objects.all().filter(status=True)
            mylist=zip(attendancedata,mechanicdata)
            return render(request,'admin/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'admin/admin_view_attendance_ask_date.html',{'form':form})

@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'admin/admin_report.html',context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'admin/admin_feedback.html',{'feedback':feedback})

@login_required(login_url='adminlogin')
def admin_services_view(request):
    return render(request,'admin/admin_services.html')

def categories(request):
    return render(request,'admin/admin_category.html')



# def categories(request):
#    categories = Category.objects.all()
#    return render(request, 'admin/admin_category.html', {'categories': categories})
def category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')  # Redirect to a success page or category list
        else:
            form = CategoryForm()


#  Employee


# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
def mechanic_dashboard_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing Done').count()
    new_work_assigned=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Approved').count()
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_work_assigned':new_work_assigned,
    'salary':mechanic.salary,
    'mechanic':mechanic,
    }
    return render(request,'Employee/mechanic_dashboard.html',context=dict)


@login_required(login_url='mechaniclogin')

def mechanic_work_assigned_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    works=models.Request.objects.all().filter(mechanic_id=mechanic.id)
    return render(request,'Employee/mechanic_work_assigned.html',{'works':works,'mechanic':mechanic})


@login_required(login_url='mechaniclogin')

def mechanic_update_status_view(request,pk):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    updateStatus=forms.MechanicUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.MechanicUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/mechanic-work-assigned')
    return render(request,'Employee/mechanic_update_status.html',{'updateStatus':updateStatus,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')

def mechanic_attendance_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    attendaces=models.Attendance.objects.all().filter(mechanic=mechanic)
    return render(request,'Employee/mechanic_view_attendance.html',{'attendaces':attendaces,'mechanic':mechanic})





@login_required(login_url='mechaniclogin')

def mechanic_feedback_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'Employee/feedback_sent.html',{'mechanic':mechanic})
    return render(request,'Employee/mechanic_feedback.html',{'feedback':feedback,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')

def mechanic_salary_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(mechanic_id=mechanic.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'Employee/mechanic_salary.html',{'workdone':workdone,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')

def mechanic_profile_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    return render(request,'Employee/mechanic_profile.html',{'mechanic':mechanic})

@login_required(login_url='mechaniclogin')

def edit_mechanic_profile_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=mechanic.user_id)
    userForm=forms.MechanicUserForm(instance=user)
    mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
    mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanic':mechanic}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST,instance=user)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('mechanic-profile')
    return render(request,'Employee/edit_mechanic_profile.html',context=mydict)

def mechanic_signup_view(request):
    userForm=forms.MechanicUserForm()
    mechanicForm=forms.MechanicForm()
    mydict={'userForm':userForm,'mechanicForm':mechanicForm}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanic=mechanicForm.save(commit=False)
            mechanic.user=user
            mechanic.save()
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
        return HttpResponseRedirect('mechaniclogin')
    return render(request,'Employee/mechanicsignup.html',context=mydict)
def mechanicsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'Employee/mechanicsclick.html')

# def admin_dashboard_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     dict={
#     'total_customer':models.User.objects.filter(is_superuser=False).count(),
#     'total_mechanic':models.Mechanic.objects.all().count(),
#      'total_request':models.Request.objects.all().count(),
#     # 'total_feedback':models.Feedback.objects.all().count(),
#     'data':zip(customers,enquiry),
#     }
#     return render(request,'admin/admin_dashboard.html',context=dict)

# def admin_customer_view(request):
#     return render(request,'admin/admin_customer.html')


# def admin_view_customer_view(request):
#     customers=models.Customer.objects.all()
#     user=User.objects.filter(is_superuser=False)
#     context = {
#         'customers' : customers,
#         'user' : user
#     }
#     return render(request,'admin/admin_view_customer.html',context)
    


# def delete_customer_view(request,pk):
    
#     user=models.User.objects.get(id=pk)
#     user.delete()
    
#     return redirect('admin-view-customer')



# def update_customer_view(request,pk):
#     # customer=models.Customer.objects.get(id=pk)
#     user=models.User.objects.get(id=pk)
#     userForm=forms.CustomerUserForm(instance=user)
#     customerForm=forms.CustomerUserForm(request.FILES,instance=user)
#     mydict={'userForm':userForm,'customerForm':customerForm}
#     if request.method=='POST':
#         userForm=forms.CustomerUserForm(request.POST,instance=user)
#         customerForm=forms.CustomerForm(request.POST,request.FILES,instance=user)
#         if userForm.is_valid() and customerForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             customerForm.save()
#             return redirect('admin-view-customer')
#     return render(request,'admin/admin_view_customer.html',context=mydict)



# def admin_add_customer_view(request):
#     userForm=forms.CustomerUserForm()
#     customerForm=forms.CustomerUserForm()
#     mydict={'userForm':userForm,'customerForm':customerForm}
#     if request.method=='POST':
#         userForm=forms.CustomerUserForm(request.POST)
#         customerForm=forms.CustomerUserForm(request.POST,request.FILES)
#         if userForm.is_valid() and customerForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             customer=customerForm.save(commit=False)
#             customer.user=user
#             customer.save()
#             # my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
#             # my_customer_group[0].user_set.add(user)
#         return HttpResponseRedirect('/admin-view-customer')
#     return render(request,'admin/admin_add_customer.html',context=mydict)



# def admin_view_customer_enquiry_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     return render(request,'admin/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})



# def admin_view_customer_invoice_view(request):
#     enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
#     print(enquiry)
#     customers=[]
#     for enq in enquiry:
#         print(enq)
#         customer=models.Customer.objects.get(id=enq['customer_id'])
#         customers.append(customer)
#     return render(request,'admin/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})


# def admin_mechanic_view(request):
#     return render(request,'admin/admin_mechanic.html')



# def admin_approve_mechanic_view(request):
#     mechanics=models.Mechanic.objects.all().filter(status=False)
#     return render(request,'admin/admin_approve_mechanic.html',{'mechanics':mechanics})

# def approve_mechanic_view(request,pk):
#     mechanicSalary=forms.MechanicSalaryForm()
#     if request.method=='POST':
#         mechanicSalary=forms.MechanicSalaryForm(request.POST)
#         if mechanicSalary.is_valid():
#             mechanic=models.Mechanic.objects.get(id=pk)
#             mechanic.salary=mechanicSalary.cleaned_data['salary']
#             mechanic.status=True
#             mechanic.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-approve-mechanic')
#     return render(request,'admin/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})



# def delete_mechanic_view(request,pk):
#     mechanic=models.Mechanic.objects.get(id=pk)
#     user=models.User.objects.get(id=mechanic.user_id)
#     user.delete()
#     mechanic.delete()
#     return redirect('admin-approve-mechanic')


# def admin_add_mechanic_view(request):
#     userForm=forms.MechanicUserForm()
#     mechanicForm=forms.MechanicForm()
#     mechanicSalary=forms.MechanicSalaryForm()
#     mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanicSalary':mechanicSalary}
#     if request.method=='POST':
#         userForm=forms.MechanicUserForm(request.POST)
#         mechanicForm=forms.MechanicForm(request.POST,request.FILES)
#         mechanicSalary=forms.MechanicSalaryForm(request.POST)
#         if userForm.is_valid() and mechanicForm.is_valid() and mechanicSalary.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             mechanic=mechanicForm.save(commit=False)
#             mechanic.user=user
#             mechanic.status=True
#             mechanic.salary=mechanicSalary.cleaned_data['salary']
#             mechanic.save()
#             # my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
#             # my_mechanic_group[0].user_set.add(user)
#             return HttpResponseRedirect('admin-view-mechanic')
#         else:
#             print('problem in form')
#     return render(request,'admin/admin_add_mechanic.html',context=mydict)



# def admin_view_mechanic_view(request):
#     mechanics=models.Mechanic.objects.all()
#     return render(request,'admin/admin_view_mechanic.html',{'mechanics':mechanics})



# def delete_mechanic_view(request,pk):
#     mechanic=models.Mechanic.objects.get(id=pk)
#     user=models.User.objects.get(id=mechanic.user_id)
#     user.delete()
#     mechanic.delete()
#     return redirect('admin-view-mechanic')



# def update_mechanic_view(request,pk):
#     mechanic=models.Mechanic.objects.get(id=pk)
#     user=models.User.objects.get(id=mechanic.user_id)
#     userForm=forms.MechanicUserForm(instance=user)
#     mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
#     mydict={'userForm':userForm,'mechanicForm':mechanicForm}
#     if request.method=='POST':
#         userForm=forms.MechanicUserForm(request.POST,instance=user)
#         mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
#         if userForm.is_valid() and mechanicForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             mechanicForm.save()
#             return redirect('admin-view-mechanic')
#     return render(request,'admin/update_mechanic.html',context=mydict)


# def admin_view_mechanic_salary_view(request):
#     mechanics=models.Mechanic.objects.all()
#     return render(request,'admin/admin_view_mechanic_salary.html',{'mechanics':mechanics})


# def update_salary_view(request,pk):
#     mechanicSalary=forms.MechanicSalaryForm()
#     if request.method=='POST':
#         mechanicSalary=forms.MechanicSalaryForm(request.POST)
#         if mechanicSalary.is_valid():
#             mechanic=models.Mechanic.objects.get(id=pk)
#             mechanic.salary=mechanicSalary.cleaned_data['salary']
#             mechanic.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-view-mechanic-salary')
#     return render(request,'admin/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})



# def admin_request_view(request):
#     return render(request,'admin/admin_request.html')


# def admin_view_request_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     return render(request,'admin/admin_view_request.html',{'data':zip(customers,enquiry)})



# def change_status_view(request,pk):
#     adminenquiry=forms.AdminApproveRequestForm()
#     if request.method=='POST':
#         adminenquiry=forms.AdminApproveRequestForm(request.POST)
#         if adminenquiry.is_valid():
#             enquiry_x=models.Request.objects.get(id=pk)
#             enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
#             enquiry_x.cost=adminenquiry.cleaned_data['cost']
#             enquiry_x.status=adminenquiry.cleaned_data['status']
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-view-request')
#     return render(request,'admin/admin_approve_request_details.html',{'adminenquiry':adminenquiry})



# def admin_delete_request_view(request,pk):
#     requests=models.Request.objects.get(id=pk)
#     requests.delete()

# def admin_add_request_view(request):
#     enquiry=forms.RequestForm()
#     adminenquiry=forms.AdminRequestForm()
#     mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
#     if request.method=='POST':
#         enquiry=forms.RequestForm(request.POST)
#         adminenquiry=forms.AdminRequestForm(request.POST)
#         if enquiry.is_valid() and adminenquiry.is_valid():
#             enquiry_x=enquiry.save(commit=False)
#             enquiry_x.customer=adminenquiry.cleaned_data['customer']
#             enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
#             enquiry_x.cost=adminenquiry.cleaned_data['cost']
#             enquiry_x.status='Approved'
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('admin-view-request')
#     return render(request,'admin/admin_add_request.html',context=mydict)

# def admin_approve_request_view(request):
#     enquiry=models.Request.objects.all().filter(status='Pending')
#     return render(request,'admin/admin_approve_request.html',{'enquiry':enquiry})

# def approve_request_view(request,pk):
#     adminenquiry=forms.AdminApproveRequestForm()
#     if request.method=='POST':
#         adminenquiry=forms.AdminApproveRequestForm(request.POST)
#         if adminenquiry.is_valid():
#             enquiry_x=models.Request.objects.get(id=pk)
#             enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
#             enquiry_x.cost=adminenquiry.cleaned_data['cost']
#             enquiry_x.status=adminenquiry.cleaned_data['status']
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-approve-request')
#     return render(request,'admin/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




# def admin_view_service_cost_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     print(customers)
#     return render(request,'admin/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


# def update_cost_view(request,pk):
#     updateCostForm=forms.UpdateCostForm()
#     if request.method=='POST':
#         updateCostForm=forms.UpdateCostForm(request.POST)
#         if updateCostForm.is_valid():
#             enquiry_x=models.Request.objects.get(id=pk)
#             enquiry_x.cost=updateCostForm.cleaned_data['cost']
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-view-service-cost')
#     return render(request,'admin/update_cost.html',{'updateCostForm':updateCostForm})




# def admin_mechanic_attendance_view(request):
#     return render(request,'admin/admin_mechanic_attendance.html')



# def admin_take_attendance_view(request):
#     mechanics=models.Mechanic.objects.all().filter(status=True)
#     aform=forms.AttendanceForm()
#     if request.method=='POST':
#         form=forms.AttendanceForm(request.POST)
#         if form.is_valid():
#             Attendances=request.POST.getlist('present_status')
#             date=form.cleaned_data['date']
#             for i in range(len(Attendances)):
#                 AttendanceModel=models.Attendance()
                
#                 AttendanceModel.date=date
#                 AttendanceModel.present_status=Attendances[i]
#                 print(mechanics[i].id)
#                 print(int(mechanics[i].id))
#                 mechanic=models.Mechanic.objects.get(id=int(mechanics[i].id))
#                 AttendanceModel.mechanic=mechanic
#                 AttendanceModel.save()
#             return redirect('admin-view-attendance')
#         else:
#             print('form invalid')
#     return render(request,'admin/admin_take_attendance.html',{'mechanics':mechanics,'aform':aform})

# def admin_view_attendance_view(request):
#     form=forms.AskDateForm()
#     if request.method=='POST':
#         form=forms.AskDateForm(request.POST)
#         if form.is_valid():
#             date=form.cleaned_data['date']
#             attendancedata=models.Attendance.objects.all().filter(date=date)
#             mechanicdata=models.Mechanic.objects.all().filter(status=True)
#             mylist=zip(attendancedata,mechanicdata)
#             return render(request,'admin/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
#         else:
#             print('form invalid')
#     return render(request,'admin/admin_view_attendance_ask_date.html',{'form':form})

# def admin_report_view(request):
#     reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
#     dict={
#         'reports':reports,
#     }
#     return render(request,'admin/admin_report.html',context=dict)



# def admin_feedback_view(request):
#     feedback=models.Feedback.objects.all().order_by('-id')
#     return render(request,'admin/admin_feedback.html',{'feedback':feedback})

# # def categories(request):
# #     return render(request,'admin/categories.html')
# def categories(request):
#     categories = Category.objects.all()
#     return render(request, 'admin/categories.html', {'categories': categories})
# def subcategory(request):
#     return render(request,'admin/subcategory.html')

# def addproduct(request):
#     categories = Category.objects.filter(status=False)
#     # seller = Seller.objects.get(user=request.user)
#     selected_category = None
#     selected_subcategory = None  # Initialize selected_subcategory to None
#     subcategories = Subcategory.objects.none()  # Initialize subcategories queryset

#     if request.method == 'POST':
#         category_id = request.POST.get('category')
#         subcategory_id = request.POST.get('subcategory')

#         try:
#             category = Category.objects.get(pk=category_id)
#             selected_category = category

#             if subcategory_id:
#                 try:
#                     subcategory = Subcategory.objects.get(pk=subcategory_id)
#                     selected_subcategory = subcategory
#                 except Subcategory.DoesNotExist:
#                     messages.error(request, 'Selected subcategory not found.')
#                     return redirect('productlist')

#             slug = request.POST.get('slug')
#             name = request.POST.get('name')
#             product_image = request.FILES.get('product_image')
#             description = request.POST.get('description')
#             quantity = request.POST.get('quantity')
#             original_price = request.POST.get('original_price')
#             selling_price = request.POST.get('selling_price')
            
#             existing_product = Product.objects.filter(name=name, seller=seller, subcategory=selected_subcategory).first()
#             if existing_product:
#                 if existing_product.status == True:
#                 # If the category exists and its status is False, update its status to True
#                     existing_product.slug = slug
#                     existing_product.product_image = product_image
#                     existing_product.description = description
#                     existing_product.quantity = quantity
#                     existing_product.original_price = original_price
#                     existing_product.selling_price = selling_price
#                     existing_product.status = False
#                     existing_product.save()
#                     messages.success(request, 'Product Added successfully.')
#                     return redirect('productlist')
#                 else:
              
#                     messages.warning(request, 'Product Already Exists.')
#                     return redirect('productlist')

#             else:
#                  product = Product.objects.create(
#                  subcategory=selected_subcategory,
#                 #  seller=seller,
#                  slug=slug,
#                  name=name,
#                  product_image=product_image,
#                  description = description,
#                  quantity = quantity,
#                  original_price=original_price,
#                  selling_price=selling_price
            
#                  )   
#                  messages.success(request, 'Product Added Successfully.')
#                  return redirect('productlist')      

#         except Category.DoesNotExist:
#             messages.error(request, 'Selected category not found.')

#     context = {
#         'categories': categories,
#         'subcategories': subcategories,
#         'selected_category': selected_category,
#         'selected_subcategory': selected_subcategory, 
#     }
    
#     return render(request, 'admin/categories.html', context)
# # def categories(request):
    
# #     if request.method == 'POST':
# #         slug = request.POST['slug']
# #         name = request.POST['name']
# #         # image = request.FILES['image']
# #         description = request.POST['description']

# #         existing_category = Category.objects.filter(slug=slug).first()
# #         if existing_category:
# #             if existing_category.status == True:
# #                 existing_category.slug=slug
# #                 existing_category.name=name
# #                 # existing_category.image=image
# #                 existing_category.description=description
# #                 existing_category.status = False
# #                 existing_category.save()
# #                 messages.success(request, 'Category Added successfully.')
# #                 return redirect('categories')
# #             else:
# #                 # If the category exists and its status is already True, show a message
# #                 messages.warning(request, 'Category Already Exists.')
# #                 return redirect('categories')

# #         else:
# #             category = Category.objects.create(
# #             slug=slug,
# #             name=name,
# #             # image=image,
# #             description = description
            
# #         )   
# #             messages.success(request, 'Category Added Successfully.')
# #             return redirect('categories') 
#     # role = request.user.role  # Assuming you have a 'role' field in your CustomUser model

# #     if role == 'admin':
# #         template_name = 'MainUser/categories.html'
# #         categories = Category.objects.filter(status=False)
# #     elif role == 'seller':
# #         template_name = 'Seller/categories.html' # Redirect to the category list page
# #         categories = Category.objects.filter(status=False)
# #  # Fetch all categories
# #     context = {'categories': categories}
# #     return render(request, template_name, context)


# # def update_category(request, category_slug):
# #     category = Category.objects.get(slug=category_slug)
# #     if request.method == 'POST':
# #         name = request.POST['name']
# #         description = request.POST['description']
# #         slug = request.POST['slug']
# #         # image = request.FILES.get('image') 
# #         category = Category.objects.get(slug=category_slug)
# #         existing_category = Category.objects.filter(name=name).exclude(slug=category_slug).first()
# #         if existing_category:
# #             if existing_category.status==True:
# #                 existing_category.name=name
# #                 existing_category.description=description
# #                 existing_category.image=image
# #                 existing_category.status = False
# #                 existing_category.save()
# #                 messages.success(request, 'Category Updated successfully.')
# #                 return redirect('categories') 
# #             else:
# #                 messages.warning(request, 'A Category with this name already exists in the selected category.')
# #                 return redirect('categories')
# #         else:
# #           category.name = name
# #           category.slug = slug
# #         # category.image = request.FILES['image']
# #           category.description = description
         
# #           messages.success(request, 'Category updated successfully.')
# #         return redirect('categories')

# #     context = {'category': category}
# #     return render(request, 'MainUser/editcategory.html', context)
#  # Import your CategoryForm

# # def category(request):
# #     if request.method == 'POST':
# #         form = CategoryForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('categories')  # Redirect to a success page or category list
# #     else:
# #         form = CategoryForm()
    
# #     return render(request, 'categories.html', {'categories': categories})
# def create_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()  # This will save the data to the database
#             return redirect('categories')  # Redirect to a success page or another view
#     else:
#         form = CategoryForm()

#     categories = Category.objects.all()  # Fetch all categories from the database
    
#     return render(request, 'categories.html', {'form': form, 'categories': categories})

# # def category_list(request):
# #     categories = Category.objects.all()
# #     return render(request, 'categories.html', {'categories': categories})