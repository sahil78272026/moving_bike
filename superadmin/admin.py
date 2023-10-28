from django.contrib import admin

# Register your models here.

from superadmin.models import TrackerDeviceInfo,AdminSubscription,AdminPayment


admin.site.register(AdminSubscription)
admin.site.register(TrackerDeviceInfo)
admin.site.register(AdminPayment)