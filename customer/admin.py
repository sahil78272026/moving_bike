from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from customer.models import User,MobileOTP,Profile,Material,MaterialSubtype,FirePushNotication,Coupon
class AdminUser(admin.ModelAdmin):
    list_display =['id']

# class AdminStaticEmail(admin.ModelAdmin):
#     list_display=['email','password']
    
class MyUserAdmin(UserAdmin):
    fieldsets = (
        ('Password Update', {
            'fields': ('password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Additional info', {
            'fields': ('username','role','mobile','country_code')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        
    )

    
admin.site.register(User,MyUserAdmin)
# admin.site.register(StaticEmail,AdminStaticEmail)
admin.site.register(MobileOTP)
admin.site.register(Profile)
# admin.site.register(Truck)
admin.site.register(Material)
admin.site.register(MaterialSubtype)
# admin.site.register(Trip)
admin.site.register(FirePushNotication)
admin.site.register(Coupon)
# admin.site.register(Photo)