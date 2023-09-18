from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile,Request,Mechanic,Attendance,Feedback
from . import models


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
                                                             
    # email = forms.EmailField(required=True,
    #                          widget=forms.TextInput(attrs={'placeholder': 'Email',
    #                                                        'class': 'form-control',
    #                                                        }))
    mobile = forms.CharField(max_length=15,  # You can adjust the max length as needed
                             required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Mobile',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
                                                                  
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    address = forms.CharField(max_length=255,  # You can adjust the max length as needed
                              required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Address',
                                                            'class': 'form-control',
                                                            }))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'mobile', 'password1', 'password2','address']
    def clean_first_name(self,*args,**kwargs):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2:
            raise forms.ValidationError("First name must be at least 2 characters long.")
        return first_name
        
        
class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile']

class MechanicUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class MechanicForm(forms.ModelForm):
    class Meta:
        model=models.Mechanic
        fields=['address','mobile','profile_pic','skill']

class MechanicSalaryForm(forms.Form):
    salary=forms.IntegerField();
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    contact = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'}))

    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ['first_name','contact','username', 'email','avatar']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.Request
        fields=['category','Car_no','Car_name','Car_model','Car_brand','problem_description']
        widgets = {
        'problem_description':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }

class AdminRequestForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
    customer=forms.ModelChoiceField(queryset=models.Customer.objects.all(),empty_label="Customer Name",to_field_name='id')
    mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
    cost=forms.IntegerField()

class AdminApproveRequestForm(forms.Form):
    mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
    cost=forms.IntegerField()
    stat=(('Pending','Pending'),('Approved','Approved'),('Released','Released'))
    status=forms.ChoiceField( choices=stat)


class UpdateCostForm(forms.Form):
    cost=forms.IntegerField()

class MechanicUpdateStatusForm(forms.Form):
    stat=(('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'))
    status=forms.ChoiceField( choices=stat)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['by','message']
        widgets = {
        'message':forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()

from .models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': ' Name',
                                                               'class': 'form-control',
                                                               }))
    Descripitions = forms.CharField(max_length=200,
                                required=True,
                                widget=forms.Textarea(attrs={'placeholder': 'Enter',
                                                              'class': 'form-control',
                                                              }))
    class Meta:
        model = Category
        fields = ['name', 'description']


# class AdminRequestForm(forms.Form):
#     #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
#     customer=forms.ModelChoiceField(queryset=models.Customer.objects.all(),empty_label="Customer Name",to_field_name='id')
#     # mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
#     cost=forms.IntegerField()

# class CustomerUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','email','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }
# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model=models.Customer
#         fields=['email']


# class MechanicUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }

# class MechanicForm(forms.ModelForm):
#     class Meta:
#         model=Mechanic
#         fields=['address','mobile','profile_pic']
# class MechanicSalaryForm(forms.Form):
#     salary=forms.IntegerField();



# # class CategoryForm(forms.ModelForm):
# #     class Meta:
# #         model = Category
# #         fields = ['name', 'slug', 'description', 'status', 'trending']  # Include the fields you want in the form
# class CategoryForm(forms.ModelForm):
#     name = forms.CharField(max_length=255,required=True, label='Name', widget=forms.TextInput(attrs={'placeholder':  'Name','class': 'form-control'}))
#     slug = forms.SlugField(max_length=100, label='Slug', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
#     class Meta:
#         model = Category
#         fields = ['name', 'slug', 'description']