from django.db import models
from django.contrib.auth.models import User


from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class Mechanic(models.Model):
    JOB_CHOICES = (
        ('mechanic', 'Mechanic'),
        ('painter', 'Painter'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MechanicProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    job_title = models.CharField(max_length=20, choices=JOB_CHOICES, default='select title')
    skill = models.CharField(max_length=500,null=True)
    salary=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Request(models.Model):


    
    cat=(('two wheeler with gear','two wheeler with gear'),('two wheeler without gear','two wheeler without gear'),('three wheeler','three wheeler'),('four wheeler','four wheeler'))
    category=models.CharField(max_length=50,choices=cat)

    vehicle_no=models.PositiveIntegerField(null=False)
    vehicle_name = models.CharField(max_length=40,null=False)
    vehicle_model = models.CharField(max_length=40,null=False)
    vehicle_brand = models.CharField(max_length=40,null=False)

    problem_description = models.CharField(max_length=500,null=False)
    date=models.DateField(auto_now=True)
    cost=models.PositiveIntegerField(null=True)

    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    mechanic=models.ForeignKey('Mechanic',on_delete=models.CASCADE,null=True)

    stat=(('Pending','Pending'),('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'),('Released','Released'))
    status=models.CharField(max_length=50,choices=stat,default='Pending',null=True)

    def __str__(self):
        return self.problem_description

class Attendance(models.Model):
    mechanic=models.ForeignKey('Mechanic',on_delete=models.CASCADE,null=True)
    date=models.DateField()
    present_status = models.CharField(max_length=10)

class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)

# category
class Category(models.Model):
    name = models.CharField(max_length=100)
    # description = models.TextField()

    def __str__(self):
        return self.name
#subcategory
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    # description = models.TextField()

    def __str__(self):
        return self.name
#subsubcategory means my service
class SubSubcategory(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='subsubcategories/', null=True, blank=True)  # Add an image field
    description = models.TextField(null=True, blank=True)  # Add a description field
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add a price field
    hours_taken = models.PositiveIntegerField(null=True, blank=True)  # Add hours taken field
    
    def __str__(self):
        return self.name
    
class CarModel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return self.name
class CarName(models.Model):
    name = models.CharField(max_length=100)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='type_images/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    # service_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    name = models.CharField(max_length=100)
    address = models.TextField()
    Alternative_mobile = models.CharField(max_length=20)
    selected_service_image = models.ImageField(upload_to='service_images/')
    selected_service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    
    selected_subsubcategory = models.ForeignKey(SubSubcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    