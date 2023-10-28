from django.db import models
from customer.models import User, Material, MaterialSubtype, Coupon
from customer.custom_azure import AzureMediaStorage as AMS
import uuid

# Create your models here.
class AdminProfile(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        
    )
    image = models.ImageField(upload_to='profile_pictures/',default='profile_pictures/default.png',storage=AMS, null=True, blank=True)
    gst=models.CharField(max_length=255,null=True,blank=True)
    pan_number=models.CharField(max_length=10,null=True,blank=True)
    company_name=models.CharField(max_length=255,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    resedential_proof=models.ImageField(upload_to='admin_documents/',storage=AMS,null=True,blank=True)
    village=models.CharField(max_length=500,null=True,blank=True)
    city=models.CharField(max_length=500,null=True,blank=True)
    state=models.CharField(max_length=500,null=True,blank=True)
    pincode=models.CharField(max_length=6,null=True,blank=True)
    resedential_proof=models.ImageField(upload_to='admin_documents/',storage=AMS,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True )
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    
    
    def __str__(self):
        return str(self.user.first_name)
    
    class Meta:
        db_table = "admin_profile"

    
    
class Truck(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_id',null=True,blank=True)
    driver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='driver_id',null=True,blank=True)
    supervisor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='supervisor_id',null=True,blank=True)
    vendor_name= models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=50,null=True,blank=True)
    manufacturer=models.CharField(max_length=50,null=True,blank=True)
    chassis_no=models.CharField(max_length=50,null=True,blank=True)
    container_no=models.CharField(max_length=30,null=True,blank=True)
    rc=models.ImageField(upload_to='rc/',default=None,storage=AMS, null=True, blank=True)
    rc1=models.ImageField(upload_to='rc/',default="jack.jpg",storage=AMS, null=True, blank=True)
    registration_date=models.CharField(max_length=30,null=True,blank=True)
    rc_expiry=models.CharField(max_length=20,null=True,blank=True)
    pollution_certificate=models.ImageField(upload_to='pollution_certificate/',default=None,storage=AMS, null=True, blank=True)
    pollution_certificate1=models.ImageField(upload_to='pollution_certificate/',default="jack.jpg",storage=AMS, null=True, blank=True)
    pollution_expiry=models.CharField(max_length=20,null=True,blank=True)
    capacity=models.FloatField(null=True,blank=True)
    height=models.IntegerField(null=True,blank=True)
    width=models.IntegerField(null=True,blank=True)
    tyre_count=models.IntegerField(null=True,blank=True)
    truck_no = models.CharField(max_length=50,null=True,blank=True)
    tracker_id = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=50,null=True,blank=True)
    avail_status=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) +" "+str(self.type)+" "+str(self.truck_no)
    
    class Meta:
        db_table = "truck"
    

class AddDriver(models.Model):
    admin=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin')
    driver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='drivers')
    status=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "add_driver"
#######################    remove this model    #####################################
# class AdminUsers(models.Model):
#     admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='admin_id')
#     user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="cstomer_user")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = "add_admin_user"
    
class AdminAccounts(models.Model):
    admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='id_admin')
    supervisor=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='id_supervisor')
    is_deleted=models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "add_admin_account"


class Trip(models.Model):
    STATUS = (
        
        ('accepted', 'accepted'),
        ('declined', 'declined'),
        ('requested','requested'),
        ('ongoing','ongoing'),
        ('upcoming','upcoming'),
        ('completed','completed')
    )
    PAYMENT_STATUS=(
        ('done','done'),
        ('pending','pending')
    )  
    id=models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    starting_point=models.TextField(blank = True,null=True)
    destination = models.TextField(blank = True,null=True)
    material=models.ForeignKey(Material, on_delete=models.CASCADE, related_name='Trip',null=True,blank=True)
    coupon=models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='Coupon',null=True,blank=True)
    truck=models.ForeignKey("Truck", on_delete=models.CASCADE,related_name='Truck',null=True,blank=True)
    other_constraints=models.CharField(max_length=100,null=True,blank=True)
    truck_type=models.CharField(max_length=30,null=True,blank=True)
    submaterial=models.ForeignKey(MaterialSubtype, on_delete=models.CASCADE, related_name='constraints',null=True,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='constraints',null=True,blank=True)
    admin=models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_id',null=True,blank=True,default="60222bea-d9b2-43c5-9ad0-585c60264e76")
    trip_status=models.CharField(max_length=20,choices=STATUS,default='requested')
    starting_date=models.CharField(max_length=20,null=True,blank=True)
    end_date=models.CharField(max_length=20,null=True,blank=True)
    amount=models.IntegerField(null=True,blank=True)
    amount_paid=models.IntegerField(null=True,blank=True)
    helpiline_no=models.IntegerField(default=129000000)
    starting_time=models.CharField(max_length=20,null=True,blank=True)
    payment_status=models.CharField(max_length=20,choices=PAYMENT_STATUS,default='pending')
    feedback=models.TextField(blank=True,null=True)
    rating=models.FloatField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    payment_date = models.DateTimeField(null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_signature=models.CharField(max_length=100,null=True,blank=True)
    gst_percent=models.IntegerField(null=True,blank=True)
    issue=models.TextField(blank=True,null=True)
    payment_issue=models.TextField(blank=True,null=True)
    truck_driver=models.ForeignKey(User, on_delete=models.CASCADE, related_name='truck_driver_id',null=True,blank=True)
    driver_start_otp=models.CharField(max_length=9, blank=True, null=True)
    #otp_time=models.DateTimeField(auto_now=True,null=True,blank=True)
    driver_otp_time=models.CharField(max_length=50, blank=True, null=True)
    driver_trip_start_date = models.DateTimeField(null=True,blank=True)
    driver_trip_complete_date = models.DateTimeField(null=True,blank=True)
    driver_complete_otp_time=models.CharField(max_length=50, blank=True, null=True)
    driver_complete_otp=models.CharField(max_length=9, blank=True, null=True)
    invoice = models.FileField(upload_to="invoice/",storage=AMS, null=True, blank=True)
    trip_id_show=models.CharField(max_length=15,unique=True,null=True,blank=True)
    gst = models.DecimalField(max_digits=100, decimal_places=2, null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.trip_id_show:
        # Generate trip id
            start = self.starting_point[:2]
            end = self.destination[:2]
            uuid_part = str(self.id)[:6]
            self.trip_id_show = (start + end + uuid_part).upper()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = "trip"

class AdminResponse(models.Model):
    CHOICES=(
        ('accept','accept'),
        ('declined','declined')
    )  
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,null=True,blank=True)
    admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    response=models.CharField(choices=CHOICES,max_length=100)
    proposed_amount=models.FloatField(null=True,blank=True)
    transit_time=models.FloatField(null=True,blank=True)
    customer_response=models.CharField(choices=CHOICES,max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "adminresponse"

# class AdminTrip(models.Model):
#     STATUS = (
        
#         ('accepted', 'accepted'),
#         ('declined', 'declined'),
#         ('requested','requested'),
#         ('ongoing','ongoing'),
#         ('upcoming','upcoming'),
#         ('completed','completed')
#     )
#     admin=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin_user_id',null=True,blank=True)
#     trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='trip_id',null=True,blank=True)
#     trip_status=models.CharField(choices=STATUS,max_length=100)
#     class Meta:
#         db_table = "admintrip"
class AdminTripDetails(models.Model):
    STATUS = (
        
        ('accepted', 'accepted'),
        ('declined', 'declined'),
        ('requested','requested'),
        ('ongoing','ongoing'),
        ('upcoming','upcoming'),
        ('completed','completed')
    )
    admin=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin_user_id',null=True,blank=True)
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='trip_id',null=True,blank=True)
    trip_status=models.CharField(choices=STATUS,max_length=100,default='requested')
    class Meta:
        db_table = "admin_trip_details"