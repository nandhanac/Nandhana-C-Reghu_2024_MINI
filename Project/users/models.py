from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django import forms




# Extending User Model Using a One-To-One Link
# class Category(models.Model):
#     slug = models.CharField(max_length=50, null=False, blank=False)
#     name=models.CharField(max_length=50, null=False, blank=False)
#     # image=models.ImageField(upload_to="category_images", null=False, blank=False)
#     status=models.BooleanField(default=False, help_text="0=default,1=Hidden")
#     trending=models.BooleanField(default=False, help_text="0=default,1=Hidden")
#     description=models.CharField(max_length=500, null=False, blank=False, default="Default description")
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Car_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
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

class Request(models.Model):
    cat=(('Diagnostic services','Diagnostic services'),('Denting  & painting','Denting  & painting'))
    category=models.CharField(max_length=50,choices=cat)

    Car_no=models.PositiveIntegerField(null=False)
    Car_name = models.CharField(max_length=40,null=False)
    Car_model = models.CharField(max_length=40,null=False)
    Car_brand = models.CharField(max_length=40,null=False)

    problem_description = models.CharField(max_length=500,null=False)
    date=models.DateField(auto_now=True)
    cost=models.PositiveIntegerField(null=True)

    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    mechanic=models.ForeignKey('Mechanic',on_delete=models.CASCADE,null=True)

    stat=(('Pending','Pending'),('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'),('Released','Released'))
    status=models.CharField(max_length=50,choices=stat,default='Pending',null=True)

    def __str__(self):
        return self.problem_description


class Mechanic(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MechanicProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
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

class Attendance(models.Model):
    mechanic=models.ForeignKey('Mechanic',on_delete=models.CASCADE,null=True)
    date=models.DateField()
    present_status = models.CharField(max_length=10)

class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)




class Category(models.Model):
    name = models.CharField(max_length=255)
    # slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

# class Customer(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     # profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
#     # address = models.CharField(max_length=40)
#     email = models.EmailField(max_length=20,null=True)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_instance(self):
#         return self
#     def __str__(self):
#         return self.user.first_name

# class Mechanic(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     profile_pic= models.ImageField(upload_to='profile_pic/MechanicProfilePic/',null=True,blank=True)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=False)
#     skill = models.CharField(max_length=500,null=True)
#     salary=models.PositiveIntegerField(null=True)
#     status=models.BooleanField(default=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_first_name(self):
#         return self.user.first_name
#     @property
#     def get_last_name(self):
#         return self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
#     def __str__(self):
#         return self.user.first_name



# class Request(models.Model):
#     cat=(('two wheeler with gear','two wheeler with gear'),('two wheeler without gear','two wheeler without gear'),('three wheeler','three wheeler'),('four wheeler','four wheeler'))
#     category=models.CharField(max_length=50,choices=cat)

#     vehicle_no=models.PositiveIntegerField(null=False)
#     vehicle_name = models.CharField(max_length=40,null=False)
#     vehicle_model = models.CharField(max_length=40,null=False)
#     vehicle_brand = models.CharField(max_length=40,null=False)

#     problem_description = models.CharField(max_length=500,null=False)
#     date=models.DateField(auto_now=True)
#     cost=models.PositiveIntegerField(null=True)

#     customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
#     # mechanic=models.ForeignKey('Mechanic',on_delete=models.CASCADE,null=True)

#     stat=(('Pending','Pending'),('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'),('Released','Released'))
#     status=models.CharField(max_length=50,choices=stat,default='Pending',null=True)

#     def __str__(self):
#         return self.problem_description
    

# class CustomerUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }

# class Category(models.Model):
#     slug = models.CharField(max_length=50, null=False, blank=False)
#     name=models.CharField(max_length=50, null=False, blank=False)
#     # image=models.ImageField(upload_to="category_images", null=False, blank=False)
#     status=models.BooleanField(default=False, help_text="0=default,1=Hidden")
#     trending=models.BooleanField(default=False, help_text="0=default,1=Hidden")
#     description=models.CharField(max_length=500, null=False, blank=False, default="Default description")
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()

#     def __str__(self):
#         return self.name
    
# class Subcategory(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50, null=False, blank=False)
#     description = models.CharField(max_length=500, null=False, blank=False, default="Default subcategory description")
#     image = models.ImageField(upload_to="subcategory_images", null=False, blank=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
#     trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")

#     def __str__(self):
#         return self.name
# class Product(models.Model):
#     # category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
#     # seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
#     slug = models.CharField(max_length=100, null=False, blank=False)
#     name=models.CharField(max_length=100, null=False, blank=False)
#     product_image=models.ImageField(upload_to="product_images", null=False, blank=False)
#     description = models.CharField(max_length=500, null=False, blank=False)
#     quantity = models.IntegerField(null=False, blank=False)
#     original_price = models.FloatField(null=False, blank=False)
#     selling_price = models.FloatField(null=False, blank=False)
#     status = models.BooleanField(default=False, help_text="0=default,1=Hidden")
#     trending = models.BooleanField(default=False, help_text="0=default,1=Trending")
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)

#     def _str_(self):
#         return self.name