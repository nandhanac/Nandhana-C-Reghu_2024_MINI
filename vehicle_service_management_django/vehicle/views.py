from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import  PasswordResetView, PasswordChangeView



from .models import Category,Subcategory,SubSubcategory,CarModel,CarName, Type,Booking,Customer,Payment
from .forms import CategoryForm,SubcategoryForm,SubSubcategoryForm,CarModelForm, CarNameForm,TypeForm,BookingForm

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/index.html')
# def home(request):

#     denting_painting_category = Category.objects.get(name="Denting & Painting")

#     # Include the category ID in the context
#     context = {
#         'category_id': denting_painting_category.id,
#     }

#     return render(request, 'vehicle/customerpage.html', context)
def about(request):
     return render(request, 'website/about.html')

def home(request):
    diagnostic_category= Category.objects.get(name="Diagnostic Test")
    denting_painting_category = Category.objects.get(name="Denting & Painting")
    car_spa_category = Category.objects.get(name="Car Spa & Cleaning")
    detailing_category = Category.objects.get(name="Detailing Service")

    # Include the category names in the context
    context = {
        'category_id': denting_painting_category.id,'diagnostic_category':diagnostic_category,
        'denting_painting_category_name': denting_painting_category.name,
        'car_spa_category_name': car_spa_category.name,
        'detailing_category_name': detailing_category.name,
    }

    return render(request, 'vehicle/customerpage.html', context)



def service_one(request):
    subsubcategories = SubSubcategory.objects.all()
    car_models = CarModel.objects.all()
    return render(request, 'website/service_one.html', {'subsubcategories': subsubcategories,'car_models': car_models})
    # return render(request, 'website/service.html')
# def service_two(request):
#     # Filter subsubcategories with front_side=True
#     front_subsubcategories = SubSubcategory.objects.filter(front_side=True)[:2]  # Limit to 2 items

#     return render(request, 'website/service_two.html', {'subsubcategories': front_subsubcategories})

# def service_two(request, category_id):
#     # Retrieve the category based on the category_id
#     category = get_object_or_404(Category, id=category_id)
#     print(category)
#     # Retrieve the subcategories and subsubcategories associated with the category
#     subcategories = Subcategory.objects.filter(category=category)
#     print(subcategories)
#     subsubcategories = SubSubcategory.objects.filter(subcategory__category=category)
#     print(subsubcategories)
#     # Pass the category, subcategories, and subsubcategories to the template
#     context = {
#         'category': category,
#         'subcategories': subcategories,
#         'subsubcategories': subsubcategories,
#     }

#     return render(request, 'website/service_two.html', context)


def service_two(request, category_id):
    # Retrieve the category based on the category_id
    category = get_object_or_404(Category, id=category_id)

    # Retrieve the subcategories associated with the category
    subcategories = Subcategory.objects.filter(category=category)

    # Prepare a dictionary where keys are subcategories and values are lists of subsubcategories
    subcategories_with_subsubcategories = {}
    for subcategory in subcategories:
        subsubcategories = SubSubcategory.objects.filter(subcategory=subcategory)
        subcategories_with_subsubcategories[subcategory] = subsubcategories

    # Pass the category and the dictionary to the template
    context = {
        'category': category,
        'subcategories_with_subsubcategories': subcategories_with_subsubcategories,
    }

    return render(request, 'website/service_two.html', context)



def service_three(request):
    # Retrieve the "Car Spa & Cleaning" category
    car_spa_category = get_object_or_404(Category, name="Car Spa & Cleaning")

    # Retrieve the subcategories associated with the "Car Spa & Cleaning" category
    subcategories = Subcategory.objects.filter(category=car_spa_category)

    # Prepare a dictionary where keys are subcategories and values are lists of subsubcategories
    subcategories_with_subsubcategories = {}
    for subcategory in subcategories:
        subsubcategories = SubSubcategory.objects.filter(subcategory=subcategory)
        subcategories_with_subsubcategories[subcategory] = subsubcategories

    # Pass the "Car Spa & Cleaning" category and the dictionary to the template
    context = {
        'car_spa_category': car_spa_category,
        'subcategories_with_subsubcategories': subcategories_with_subsubcategories,
    }

    return render(request, 'website/service_three.html', context)

def service_four(request):
    # Retrieve the "Car Spa & Cleaning" category
    detailing_category = get_object_or_404(Category, name="Detailing Service")

    # Retrieve the subcategories associated with the "Car Spa & Cleaning" category
    subcategories = Subcategory.objects.filter(category=detailing_category)

    # Prepare a dictionary where keys are subcategories and values are lists of subsubcategories
    subcategories_with_subsubcategories = {}
    for subcategory in subcategories:
        subsubcategories = SubSubcategory.objects.filter(subcategory=subcategory)
        subcategories_with_subsubcategories[subcategory] = subsubcategories

    # Pass the "Car Spa & Cleaning" category and the dictionary to the template
    context = {
        'detailing_category': detailing_category,
        'subcategories_with_subsubcategories': subcategories_with_subsubcategories,
    }

    return render(request, 'website/service_four.html', context)


# def selectcar(request):
#     car_models = CarModel.objects.all()
#     return render(request,'website/select_car.html',{'car_models': car_models,})

# def selectcar(request,subsubcategory_id):
#      subsubcategory = get_object_or_404(SubSubcategory, pk=subsubcategory_id)
#      car_models = CarModel.objects.all()
#      create_car_name = CarName.objects.all()
#      types = Type.objects.all()
#      return render(request, 'website/select_car.html', {'car_models': car_models, 'create_car_name': create_car_name, 'types': types, 'subsubcategory': subsubcategory})



def selectcar(request, subsubcategory_id):
    subsubcategory = get_object_or_404(SubSubcategory, pk=subsubcategory_id)
    
    # Fetch all car models
    car_models = CarModel.objects.all()

    # Create a dictionary to store car names by car model
    car_names_by_model = {}

    for car_model in car_models:
        # Get car names associated with the car model
        car_names = CarName.objects.filter(car_model=car_model)
        car_names_by_model[car_model] = car_names

    # Fetch all types (not sure if you need this for printing)
    types = Type.objects.all()

    # Render the 'select_car.html' template and pass the data
    return render(request, 'website/select_car.html', {'car_models': car_models, 'car_names_by_model': car_names_by_model, 'types': types, 'subsubcategory': subsubcategory})







def create_car_name(request):
    if request.method == 'POST':
        form = CarNameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_car_name')
    else:
        form = CarNameForm()
    
    create_car_name = CarName.objects.all()
    return render(request, 'vehicle/admin_car.html', {'form': form, 'create_car_name': create_car_name})

def delete_car_name(request, car_name_id):
    car_name = get_object_or_404(CarName, pk=car_name_id)
    # if request.method == 'POST':
    car_name.delete()
    return redirect('create_car_name')
    # return render(request, 'vehicle/admin_car.html', {'car_name': car_name})


def types(request):
    if request.method == 'POST':
        form = TypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = TypeForm()

    types = Type.objects.all()
    return render(request, 'vehicle/admin_type.html', {'form': form, 'types': types})


# def service_booking(request, subsubcategory_id):
#     subsubcategory = SubSubcategory.objects.get(id=subsubcategory_id)
#     categories = Category.objects.all()
#     subcategories = Subcategory.objects.all()

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or do something else
#     else:
#         form = BookingForm()

#     context = {
#         'subsubcategory': subsubcategory,
#         'categories': categories,
#         'subcategories': subcategories,
#         'form': form,
#     }

#     return render(request, 'website/booking.html', context)



#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/customerclick.html')

#for showing signup/login button for mechanics
def mechanicsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/mechanicsclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')
    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'Password/password_reset.html'
    email_template_name = 'Password/password_reset_email.html'
    subject_template_name = 'Password/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'Password/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

def customer_signup_view(request):
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
        return HttpResponseRedirect('customerlogin')
    return render(request,'vehicle/customersignup.html',context=mydict)


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
    return render(request,'vehicle/mechanicsignup.html',context=mydict)


#for checking user customer, mechanic or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_mechanic(user):
    return user.groups.filter(name='MECHANIC').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('users-home')
    elif is_mechanic(request.user):
        accountapproval=models.Mechanic.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('mechanic-dashboard')
        else:
            return render(request,'vehicle/mechanic_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')




#============================================================================================
# ADMIN RELATED views start
#============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    booking = Booking.objects.all()
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Booking.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)
#  service
@login_required(login_url='adminlogin')
def admin_service_view(request):
    return render(request,'vehicle/admin_service.html')
@login_required(login_url='adminlogin')
def admin_category_view(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('admin-category')
    else:
        form = CategoryForm()

    return render(request, 'vehicle/admin_category.html', {'categories': categories, 'form': form})



# Edit view
@login_required(login_url='adminlogin')
def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin-category')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'vehicle/update_category.html', {'form': form})

# Delete view
@login_required(login_url='adminlogin')
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    # if request.method == 'POST':
    category.delete()
    return redirect('admin-category')
    
    # return render(request, 'vehicle/admin_category.html', {'category': category})

@login_required(login_url='adminlogin')
def admin_subcategory_view(request):
    # category = get_object_or_404(Category, pk=category_id)
    subcategories = Subcategory.objects.all()

    if request.method == 'POST':
        print("got")
        subcategory_form = SubcategoryForm(request.POST)
        print(subcategory_form)
        if subcategory_form.is_valid():
         subcategory = subcategory_form.save(commit=False)
         subcategory.save()
         print("Saved")
         return redirect('admin_subcategory_view')
        else:
         print('Form Errors:', subcategory_form.errors)
    else:
        print('Wrong')
        subcategory_form = SubcategoryForm()

    return render(request, 'vehicle/admin_subcategory.html', { 'subcategories': subcategories, 'subcategory_form': subcategory_form})
def update_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)

    if request.method == 'POST':
        subcategory_form = SubcategoryForm(request.POST, instance=subcategory)
        if subcategory_form.is_valid():
            subcategory_form.save()
            return redirect('admin_subcategory_view')
    else:
        subcategory_form = SubcategoryForm(instance=subcategory)

    return render(request, 'vehicle/update_subcategory.html', {'subcategory_form': subcategory_form})

def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    subcategory.delete()
    return redirect('admin_subcategory_view')
@login_required(login_url='adminlogin')
def admin_subsubcategory_view(request):
    # subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    subsubcategories = SubSubcategory.objects.all()

    if request.method == 'POST':
        subsubcategory_form = SubSubcategoryForm(request.POST, request.FILES)
        if subsubcategory_form.is_valid():
            subsubcategory = subsubcategory_form.save(commit=False)
            # subsubcategory.subcategory = subcategory
            subsubcategory.save()
            print("Saved")
            return redirect('admin_subsubcategory_view')
        else:
         print('Form Errors:', subsubcategory_form.errors)
    else:
        print('Wrong')
        subsubcategory_form = SubSubcategoryForm()

    return render(request, 'vehicle/admin_subsubcategory.html', { 'subsubcategories': subsubcategories, 'subsubcategory_form': subsubcategory_form })
@login_required(login_url='adminlogin')
def update_subsubcategory_view(request, subsubcategory_id):
    subsubcategory = get_object_or_404(SubSubcategory, id=subsubcategory_id)
    
    if request.method == 'POST':
        subsubcategory_form = SubSubcategoryForm(request.POST, request.FILES, instance=subsubcategory)
        if subsubcategory_form.is_valid():
            subsubcategory_form.save()
            return redirect('admin_subsubcategory_view')
    else:
        subsubcategory_form = SubSubcategoryForm(instance=subsubcategory)
    
    return render(request, 'vehicle/update_subsubcategory.html', {'subsubcategory_form': subsubcategory_form, 'subsubcategory': subsubcategory})     

@login_required(login_url='adminlogin')
def delete_subsubcategory_view(request, subsubcategory_id):
    subsubcategory = get_object_or_404(SubSubcategory, id=subsubcategory_id)
    
    if request.method == 'POST':
        subsubcategory.delete()
        return redirect('admin_subsubcategory_view')
    
    return render(request, 'vehicle/delete_subsubcategory.html', {'subsubcategory': subsubcategory})



def car_models(request):
    car_models = CarModel.objects.all()
    
    if request.method == 'POST':
        form = CarModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car-models')  # Redirect to the same page after form submission

    else:
        form = CarModelForm()

    return render(request, 'vehicle/admin_selectcar.html', {'car_models': car_models, 'form': form})











@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'vehicle/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'vehicle/admin_view_customer.html',{'customers':customers})


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
    return render(request,'vehicle/update_customer.html',context=mydict)


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
    return render(request,'vehicle/admin_add_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_mechanic_view(request):
    return render(request,'vehicle/admin_mechanic.html')


@login_required(login_url='adminlogin')
def admin_approve_mechanic_view(request):
    mechanics=models.Mechanic.objects.all().filter(status=False)
    return render(request,'vehicle/admin_approve_mechanic.html',{'mechanics':mechanics})

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
    return render(request,'vehicle/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})


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
    return render(request,'vehicle/admin_add_mechanic.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_mechanic_view(request):
    mechanics=models.Mechanic.objects.all()
    return render(request,'vehicle/admin_view_mechanic.html',{'mechanics':mechanics})


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
    return render(request,'vehicle/update_mechanic.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_mechanic_salary_view(request):
    mechanics=models.Mechanic.objects.all()
    return render(request,'vehicle/admin_view_mechanic_salary.html',{'mechanics':mechanics})

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
    return render(request,'vehicle/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'vehicle/admin_request.html')

@login_required(login_url='adminlogin')
# def admin_view_request_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     return render(request,'vehicle/admin_view_request.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    booking = Booking.objects.select_related('selected_car_model', 'selected_car_name', 'selected_type').all()
    return render(request, 'vehicle/admin_view_request.html', {'booking': booking})


@login_required(login_url='adminlogin')
def change_status_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Booking.objects.get(id=pk)
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Booking.objects.get(id=pk)
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
    return render(request,'vehicle/admin_add_request.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    booking=models.Booking.objects.all().filter(status='Pending')
    return render(request,'vehicle/admin_approve_request.html',{'booking':booking})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Booking.objects.get(id=pk)
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'vehicle/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


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
    return render(request,'vehicle/update_cost.html',{'updateCostForm':updateCostForm})



@login_required(login_url='adminlogin')
def admin_mechanic_attendance_view(request):
    return render(request,'vehicle/admin_mechanic_attendance.html')


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
    return render(request,'vehicle/admin_take_attendance.html',{'mechanics':mechanics,'aform':aform})

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
            return render(request,'vehicle/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'vehicle/admin_view_attendance_ask_date.html',{'form':form})

@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'vehicle/admin_report.html',context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'vehicle/admin_feedback.html',{'feedback':feedback})

#============================================================================================
# ADMIN RELATED views END
#============================================================================================


#============================================================================================
# CUSTOMER RELATED views start
#============================================================================================

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(customer_id=customer.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Pending") | Q(status="Approved")).count()
    bill=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_request_made':new_request_made,
    'bill':bill['cost__sum'],
    'customer':customer,
    }
    return render(request,'vehicle/customer_dashboard.html',context=dict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_request.html',{'customer':customer})




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    if request.user.is_authenticated:
        print("User is authenticated")
        print("User ID:", request.user.id)
    customer=models.Customer.objects.get(user_id=request.user.id)
    booking=models.Booking.objects.filter(customer_id=customer.id , status="Pending")
    print("Customer:", customer)  # Check if customer data is retrieved
    print("Bookings:", booking) 
    return render(request,'vehicle/customer_view_request.html',{'customer':customer,'booking':booking})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):
    customer=models.Customer.objects.get(user_id=request.user.id)
    booking=models.Booking.objects.get(id=pk)
    booking.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer = models.Customer.objects.get(user=request.user)
    booking = models.Booking.objects.filter(customer=customer).exclude(status="Pending")
    return render(request,'vehicle/customer_view_approved_request.html',{'customer':customer,'booking':booking})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    booking=models.Booking.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_view_approved_request_invoice.html',{'customer':customer,'booking':booking})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.BookingForm()
    if request.method=='POST':
        enquiry=forms.BookingForm(request.POST)
        if enquiry.is_valid():
            customer=models.Customer.objects.get(user_id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=customer
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request,'vehicle/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'vehicle/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'vehicle/customer_feedback.html',{'feedback':feedback,'customer':customer})
#============================================================================================
# CUSTOMER RELATED views END
#============================================================================================






#============================================================================================
# MECHANIC RELATED views start
#============================================================================================


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
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
    return render(request,'vehicle/mechanic_dashboard.html',context=dict)

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_work_assigned_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    works=models.Booking.objects.all().filter(mechanic_id=mechanic.id)
    return render(request,'vehicle/mechanic_work_assigned.html',{'works':works,'mechanic':mechanic})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_update_status_view(request,pk):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    updateStatus=forms.MechanicUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.MechanicUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Booking.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/mechanic-work-assigned')
    return render(request,'vehicle/mechanic_update_status.html',{'updateStatus':updateStatus,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_attendance_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    attendaces=models.Attendance.objects.all().filter(mechanic=mechanic)
    return render(request,'vehicle/mechanic_view_attendance.html',{'attendaces':attendaces,'mechanic':mechanic})





@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_feedback_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent.html',{'mechanic':mechanic})
    return render(request,'vehicle/mechanic_feedback.html',{'feedback':feedback,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_salary_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(mechanic_id=mechanic.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'vehicle/mechanic_salary.html',{'workdone':workdone,'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_profile_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    return render(request,'vehicle/mechanic_profile.html',{'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
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
    return render(request,'vehicle/edit_mechanic_profile.html',context=mydict)






#============================================================================================
# MECHANIC RELATED views start
#============================================================================================




# for aboutus and contact
def aboutus_view(request):
    return render(request,'vehicle/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'vehicle/contactussuccess.html')
    return render(request, 'vehicle/contactus.html', {'form':sub})



def book_service(request, subsubcategory_id):
    subsubcategory = get_object_or_404(SubSubcategory, pk=subsubcategory_id)
    customer = Customer.objects.get(user=request.user)
    # car_model = get_object_or_404(CarModel, pk=car_model_id)
    # car_name = get_object_or_404(CarName, pk=car_name_id)
    # type = get_object_or_404(Type, pk=type_id)

    if request.method == 'POST':
        form = BookingForm(request.POST,request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.selected_subsubcategory = subsubcategory
            booking.customer = customer
            # booking.selected_car_model = car_model
            # booking.selected_car_name = car_name
            # booking.selected_type = type
            booking.name = request.user.first_name
            booking.save()
            if booking.payment_method == 'Cash':
                return redirect('bookconfirm_cash', booking.id)
            elif booking.payment_method == 'Online':
                # Redirect to the payment page for online payment
                # Replace 'payment_page' with your actual payment page URL
                return redirect('payment_confirmation')
            
    else:
        # form = BookingForm()
        form = BookingForm(initial={'name': request.user.first_name})
    return render(request, 'website/booking.html', {'form': form, 'subsubcategory': subsubcategory})




def booking_confirmation(request, booking_id,payment_amount):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'website/booking_confirmation.html',{'booking': booking,'payment_amount':payment_amount})

def bookconfirm_cash(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'website/bookconfirm_cash.html',{'booking': booking})




import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib.auth.models import User  # Import the user model you are using

 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 

@login_required
def payment_confirmation(request):
    currency = 'INR'
    user = request.user
    customer, created = Customer.objects.get_or_create(user=user)

    # Retrieve the booking associated with the current user (you may need to adjust the query depending on your model relationships)
    booking = Booking.objects.filter(customer=customer).last()

    if booking:
        # Get the selected service's price from the booking
        selected_service_price = booking.selected_subsubcategory.price

        # Calculate the payment amount (if the service has a price)
        if selected_service_price is not None:
            amount = int(selected_service_price * 100)  # Convert to paisa
        else:
            amount = 0  # Default to 0 if price is not set
    else:
        amount = 0  # Default to 0 if there's no booking
    
    request.session['payment_amount'] = amount
    request.session['booking_id'] = booking.pk


    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Get the current user
    # Retrieve or create the associated Customer instance
    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # Create a Payment for the appointment
    payment = Payment.objects.create(
        user=customer,
        payment_amount=amount,
        payment_status='Pending',
    )

    # Render the success template with the necessary context
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
        'booking': booking,  # Pass the booking instance to the template

    }
    messages.success(request, 'Payment amount has been saved. You will be redirected to the payment page.')

    return render(request, 'website/payment_confirmation.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            # Get the payment details from the POST request
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            # amount = request.POST.get('razorpay_amount', '')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            
            if result is not None:
                # if amount:
                #     try:
                #         amount = int(amount)
                #     except ValueError:
                #         # Handle the case where 'amount' is not a valid integer
                #         amount = 0  # Set a default value or handle the error condition as needed
                # else:
                #     amount = 0  # Set a default value (0) when 'amount' is an empty string

                payment_amount = request.session.get('payment_amount', 0)
                booking_id = request.session.get('booking_id', 0)

                # Capture the payment
                razorpay_client.payment.capture(payment_id, payment_amount)
                customer = Customer.objects.get(user=request.user)

                # Save payment details to the Payment model
                # Assuming you have a Payment model defined
                payment = Payment.objects.create(
                    user=customer,  # Assign the Customer instance
                    payment_amount=payment_amount,
                    payment_status='Success',  # Assuming payment is successful
                )
                context = { 
                    'payment_amount': payment_amount,
                }
                # Redirect to a success page with payment details
                return redirect('booking_confirmation',booking_id=booking_id,payment_amount=payment_amount)  # Replace 'orders' with your actual success page name or URL
            else:
                # Signature verification failed
                return HttpResponse("Payment signature verification failed", status=400)
        except Exception as e:
            # Handle exceptions gracefully
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    else:
        # Handle non-POST requests
        return HttpResponse("Invalid request method", status=405)
    
def invoice(request,booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'website/invoice.html', {'booking': booking})

from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_invoice_pdf(request, booking_id):
    # Get the booking data
    booking = get_object_or_404(Booking, pk=booking_id)

    # Create a buffer for the PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list of flowables for the PDF content
    elements = []

    # Define custom styles
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    
    # Create custom styles
    custom_style_title = ParagraphStyle(
        name='CustomTitle',
        parent=styleH,
        fontSize=14,
        leading=18,
        textColor=colors.blue,
    )

    custom_style_subtitle = ParagraphStyle(
        name='CustomSubtitle',
        parent=styleN,
        fontSize=12,
        leading=16,
        textColor=colors.black,
    )

    # Add the title
    elements.append(Paragraph('Invoice', custom_style_title))
    elements.append(Spacer(1, 12))

    # Add booking ID and date
    elements.append(Paragraph(f'Booking ID: {booking.id}', custom_style_subtitle))
    elements.append(Paragraph(f'Booking Date: {booking.appointment_date.strftime("%d/%m/%Y")}', custom_style_subtitle))
    elements.append(Spacer(1, 12))

    # Add Invoice From information
    elements.append(Paragraph('Invoice From:', custom_style_subtitle))
    elements.append(Paragraph('SplashPaintZone', custom_style_subtitle))
    elements.append(Paragraph('123 Street, Kanjirappally, Kerala', custom_style_subtitle))
    elements.append(Spacer(1, 12))

    # Add Invoice To information
    elements.append(Paragraph('Invoice To:', custom_style_subtitle))
    elements.append(Paragraph(booking.name, custom_style_subtitle))
    elements.append(Paragraph(booking.address, custom_style_subtitle))
    elements.append(Spacer(1, 12))

    # Add Payment Method
    elements.append(Paragraph(f'Payment Method: {booking.payment_method}', custom_style_subtitle))

    # Add Payment Details and Bank Name if the method is 'Online'
    # if booking.payment_method == "Online":
    #     elements.append(Paragraph(f'Payment Details: {booking.payment_details}', custom_style_subtitle))
    #     elements.append(Paragraph(f'Bank Name: {booking.bank_name}', custom_style_subtitle))

    elements.append(Spacer(1, 12))

    # Add Description, Quantity, VAT, and Total Amount
    table_data = [
        ['Description:', booking.selected_subsubcategory.name],
        ['Quantity:', '1'],
        ['VAT:', '$0'],
        ['Total Amount:', f'${booking.selected_subsubcategory.price}'],
    ]
    table = Table(table_data, colWidths=[100, 400])
    table.setStyle(
        [
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]
    )
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add Other Information
    

    # Build the PDF document
    doc.build(elements)

    # Create a response with the PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.id}.pdf"'
    response.write(buffer.getvalue())
    buffer.close()

    return response
