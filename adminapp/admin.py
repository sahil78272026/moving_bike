from django.contrib import admin

# Register your models here.

from adminapp.models import AdminProfile,Truck, Trip


class AdminTrip(admin.ModelAdmin):
    list_display=['user_id',"id",'starting_point',"destination"]
    search_fields =["user__id","starting_point__icontains","destination__icontains","trip_status__icontains"]

admin.site.register(AdminProfile)
admin.site.register(Truck)
admin.site.register(Trip,AdminTrip)
