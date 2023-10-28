from django.contrib import admin

# Register your models here.
from driverapp.models import Document,DriverLanguage


# admin.site.register(DriverProfile)
admin.site.register(Document)
admin.site.register(DriverLanguage)