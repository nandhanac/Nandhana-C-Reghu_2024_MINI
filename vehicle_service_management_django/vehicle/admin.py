from django.contrib import admin

# Register your models here.
from .models import Attendance,Category,Subcategory,CarModel, Booking,Type,Feedback,Customer,Mechanic

admin.site.register(Customer)
admin.site.register(Attendance)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(CarModel)
admin.site.register(Booking)
admin.site.register(Type)
admin.site.register(Feedback)
admin.site.register(Mechanic)
