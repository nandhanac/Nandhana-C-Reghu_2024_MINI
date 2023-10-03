from django.contrib import admin

# Register your models here.
from .models import Attendance,Category,Subcategory,CarModel


admin.site.register(Attendance)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(CarModel)