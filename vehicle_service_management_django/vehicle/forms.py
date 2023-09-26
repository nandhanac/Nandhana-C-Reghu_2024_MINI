from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Category,Subcategory,SubSubcategory
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
        fields=['address','mobile','profile_pic']


class MechanicUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class MechanicForm(forms.ModelForm):
    job_title = forms.ChoiceField(
        choices=[('select title', 'select title'),('mechanic', 'Mechanic'), ('painter', 'Painter')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Job Title'
    )
    
    class Meta:
        model=models.Mechanic
        fields=['address','mobile','profile_pic','job_title','skill']

class MechanicSalaryForm(forms.Form):
    salary=forms.IntegerField();


class RequestForm(forms.ModelForm):
    class Meta:
        model=models.Request
        fields=['category','vehicle_no','vehicle_name','vehicle_model','vehicle_brand','problem_description']
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
    date = forms.DateField()
       


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

# category



class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            # 'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Category Description'}),
        }
class SubcategoryForm(forms.ModelForm):
    # Add a category field to select the associated category
    category = forms.ModelChoiceField(queryset=None, empty_label="Select a Category", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Subcategory
        fields = ['name', 'category']  # Include the 'category' field in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subcategory Name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset for the category field to display existing categories
        self.fields['category'].queryset = Category.objects.all()
class SubSubcategoryForm(forms.ModelForm):
    # Add fields for image, description, price, and hours taken
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}))
    hours_taken = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hours Taken'}))

    class Meta:
        model = SubSubcategory
        fields = ['name', 'subcategory', 'image', 'description', 'price', 'hours_taken']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SubSubcategory Name'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
        }