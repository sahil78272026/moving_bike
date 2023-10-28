from django.db import models
from customer.models import User
from customer.custom_azure import AzureMediaStorage as AMS
from adminapp.models import Trip
class DriverProfile(models.Model):
    """Driver Profile model."""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='driver_profile',null=True)
    alternate_phone = models.CharField(max_length=20,null=True,blank=True)
    image = models.ImageField(upload_to='profile_pictures/',default='profile_pictures/default.png',storage=AMS, null=True, blank=True)
    slug = models.SlugField(blank=True, max_length=150)
    address = models.TextField(null=True, blank=True, )
    driving_license=models.CharField(max_length=20,null=True,blank=True)
    zipcode = models.CharField(max_length=6,
                                blank=True,
                                null=True,
                                )
    city = models.CharField(max_length=50,
                            null=True,
                            blank=True,
                            )
    state = models.CharField(max_length=100,
                             null=True,
                             blank=True,
                             )
    landmark = models.CharField(max_length=100, null=True, blank=True, )
    about = models.TextField(null=True, blank=True, )
    bio = models.TextField(null=True, blank=True, )
    is_active = models.BooleanField(default=True,
                                    )
    created_at = models.DateTimeField(null=True,
                                      blank=True,
                                      )
    updated_at = models.DateTimeField(null=True,
                                      blank=True,
                                      )
    
    def __str__(self):
        return str(self.user.id)
    class Meta:
        db_table = "driver_profile"
    
# class Device_Intergrations(models.Model):
#     device=models.CharField(max_length=100,null=True,blank=True)
#     data=models.CharField(max_length=1000,null=True,blank=True)
#     humidity=models.CharField(max_length=20,null=True,blank=True)
#     motion=models.CharField(max_length=20,null=True,blank=True)
#     temp=models.CharField(max_length=20,null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True,null=True,
#                                       blank=True,
#                                       )
#     updated_at = models.DateTimeField(auto_now=True,null=True,
#                                       blank=True,
#                                       )
    
# class DeviceIntergrations(models.Model):
#     device=models.CharField(max_length=100,null=True,blank=True)
#     data=models.CharField(max_length=1000,null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True,null=True,
#                                       blank=True,
#                                       )
#     updated_at = models.DateTimeField(auto_now=True,null=True,
#                                       blank=True,)
    
class TrackerDeviceIntergrations(models.Model):
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,null=True,blank=True,default='ff4e3a09-38d6-49a0-9186-2485403b7be4',related_name="trip")
    status=models.BooleanField(default=True,null=True,blank=True)
    admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    tracker_availability=models.BooleanField(default=True,null=True,blank=True)
    device=models.CharField(max_length=100,null=True,blank=True, db_index=True)
    data=models.CharField(max_length=1000,null=True,blank=True)
    type=models.CharField(max_length=100,null=True,blank=True)
    downlink_type=models.CharField(max_length=100,null=True,blank=True)
    firmware_version=models.CharField(max_length=100,null=True,blank=True)
    hardware_version=models.CharField(max_length=100,null=True,blank=True)
    serial_no=models.CharField(max_length=100,null=True,blank=True)
    accelerometer=models.CharField(max_length=100,null=True,blank=True)
    temperature_humidity=models.CharField(max_length=100,null=True,blank=True)
    temperature_value=models.CharField(max_length=10,null=True,blank=True)
    gps=models.CharField(max_length=100,null=True,blank=True)
    fuel_gauge=models.CharField(max_length=100,null=True,blank=True)
    eeprom=models.CharField(max_length=100,null=True,blank=True)
    pressure=models.CharField(max_length=100,null=True,blank=True)
    ambient_light=models.CharField(max_length=100,null=True,blank=True)
    rfu=models.CharField(max_length=100,null=True,blank=True)
    battery_level=models.CharField(max_length=10,null=True,blank=True)
    temperature_sign=models.CharField(max_length=100,null=True,blank=True)
    temperature=models.CharField(max_length=50,null=True,blank=True)
    humidity=models.CharField(max_length=10,null=True,blank=True)
    motion_sensor=models.CharField(max_length=50,null=True,blank=True)
    position=models.CharField(max_length=50,null=True,blank=True)
    roll_angle=models.CharField(max_length=50,null=True,blank=True)
    pitch_angle=models.CharField(max_length=50,null=True,blank=True)
    lat_degree=models.CharField(max_length=100,null=True,blank=True)
    lat_min1=models.CharField(max_length=100,null=True,blank=True)
    lat_min2=models.CharField(max_length=100,null=True,blank=True)
    lat_min3=models.CharField(max_length=100,null=True,blank=True)
    lon_degree=models.CharField(max_length=100,null=True,blank=True)
    lon_min2=models.CharField(max_length=100,null=True,blank=True)
    latitude=models.CharField(max_length=100,null=True,blank=True)
    longitude=models.CharField(max_length=100,null=True,blank=True)
    mac_time=models.CharField(max_length=50,null=True,blank=True)
    alerttype=models.CharField(max_length=100,null=True,blank=True)
    tilt=models.CharField(max_length=100,null=True,blank=True)
    fall_detection=models.CharField(max_length=100,null=True,blank=True)
    theft=models.CharField(max_length=100,null=True,blank=True)
    low_battery_level=models.CharField(max_length=100,null=True,blank=True)
    alert_temperature=models.CharField(max_length=30,null=True,blank=True)
    alert_humidity=models.CharField(max_length=30,null=True,blank=True)
    old_position=models.CharField(max_length=30,null=True,blank=True)
    new_position=models.CharField(max_length=30,null=True,blank=True)
    seqNumber = models.IntegerField(default="123", null=True,blank=True,)
    timeStamp = models.DateTimeField(null=True, blank=True,)
    address=models.TextField(null=True,blank=True,default='noida sector 67')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True,)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True,)

    
    # class Meta:
    #     ordering = ('-id',)
    
    class Meta:
        db_table = "tracker_device"
    
    
class Document(models.Model):
    title=models.CharField(max_length=100,null=True,blank=True)
    expiration_date=models.DateField()
    expired=models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True,)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True,)
    
    def __str__(self):
        return str(self.title )+" "+str(self.expired)+" "+str(self.expiration_date)
    
    class Meta:
        db_table = "document"

class DriverLanguage(models.Model):
    name=models.CharField(max_length=20,null=True,blank=True)
    status=models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    def __str__(self):
        return str(self.name )
    
    class Meta:
        db_table = "language"
    
    
class GoogleLatLon(models.Model):
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,null=True,blank=True,related_name="google_trip")
    driver=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="driver")
    glat=models.CharField(max_length=200,null=True,blank=True)
    glon=models.CharField(max_length=200,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    def __str__(self) :
        return str(self.id)
    class Meta:
        db_table = "google_lat_lon"