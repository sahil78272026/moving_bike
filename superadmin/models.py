import uuid
from django.db import models
from adminapp.models import AdminProfile, Trip
from customer.models import User
# Create your models here.

class TrackerDeviceInfo(models.Model):
        admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
        type=models.CharField(max_length=20,null=True,blank=True)
        firmware_version=models.CharField(max_length=20,null=True,blank=True)
        hardware_version=models.CharField(max_length=20,null=True,blank=True)
        device=models.CharField(max_length=20,null=True,blank=True)
        serial_no=models.CharField(max_length=20,null=True,blank=True)
        tracker_availability=models.BooleanField(default=True)
        tracker_assigned=models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
        updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
        
        def __str__(self):
            return str(self.id)
    
        class Meta:
            db_table = "trackerdeviceinfo"
            
class HelpDeskQuery(models.Model):
        query_status_choices = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'), 
        )
        PRIORITY_CHOICES = (('High','High'),
                            ('Medium','Medium'),
                            ('Low','Low'))
        
        admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='admin_uuid')
        query=models.TextField()
        query_status=models.CharField(max_length=20,null=True,blank=True,choices=query_status_choices,default='New')
        priority=models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
        created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
        updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
        
        class Meta:
            db_table = "helpdeskquery"

class AdminSubscription(models.Model):
        payment_status_choice=(
            ('done','done'),
            ('pending','pending')
            )
        PAYMENT_TYPE_CHOICES = (
            ('Credit Card', 'Credit Card'),
            ('Upi', 'Upi'),
            ('Other', 'Other'),
            )
        admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
        subscription_period=models.FloatField(null=True,blank=True,default='0')
        payment_id=models.CharField(max_length=10, unique=True, blank=True)
        payment_status=models.CharField(max_length=20,null=True,blank=True,choices=payment_status_choice,default='pending')
        payment_type=models.CharField(max_length=20,null=True,blank=True,choices=PAYMENT_TYPE_CHOICES)
        mac_address = models.CharField(max_length=17)
        sub_start_date=models.CharField(max_length=30,null=True,blank=True)
        sub_end_date=models.CharField(max_length=30,null=True,blank=True)
        created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True,)
        updated_at = models.DateTimeField(auto_now=True,null=True,blank=True,)
        def save(self, *args, **kwargs):
            if not self.payment_id:
                try:
                    admin = User.objects.get(id=self.admin.id)
                    try:
                        admin_obj = AdminProfile.objects.get(user_id=admin.id)
                        company_name = admin_obj.company_name
                    except AdminProfile.DoesNotExist:
                    # Handle the case where the associated AdminProfile doesn't exist
                        company_name = ""
                except User.DoesNotExist:
                # Handle the case where the associated User doesn't exist
                    company_name = ""
                id_string = company_name[:4].upper() + uuid.uuid4().hex[:6].upper()
                
                # Keep randomizing suffix till unique
                while AdminSubscription.objects.filter(payment_id=id_string).exists():
                    id_string = company_name[:4].upper() + uuid.uuid4().hex[:6].upper()
                    
                self.payment_id = id_string
        
            super().save(*args, **kwargs)
        class Meta:
            db_table = "admin_subscription"
class AdminPayment(models.Model):
        payment_status_choice=(
            ('done','done'),
            ('pending','pending')
            )
        admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
        trip=models.ForeignKey(Trip,on_delete=models.CASCADE,null=True,blank=True)
        payment_id=models.CharField(max_length=10, unique=True, blank=True)
        amount=models.FloatField(null=True,blank=True)
        payment_status=models.CharField(max_length=20,null=True,blank=True,choices=payment_status_choice,default='pending')
        def save(self, *args, **kwargs):
            if not self.payment_id:
                try:
                    admin = User.objects.get(id=self.admin.id)
                    try:
                        admin_obj = AdminProfile.objects.get(user_id=admin.id)
                        company_name = admin_obj.company_name
                    except AdminProfile.DoesNotExist:
                    # Handle the case where the associated AdminProfile doesn't exist
                        company_name = ""
                except User.DoesNotExist:
                # Handle the case where the associated User doesn't exist
                    company_name = ""
                id_string = company_name[:4].upper() + uuid.uuid4().hex[:6].upper()
                
                # Keep randomizing suffix till unique
                while AdminSubscription.objects.filter(payment_id=id_string).exists():
                    id_string = company_name[:4].upper() + uuid.uuid4().hex[:6].upper()
                    
                self.payment_id = id_string
        
            super().save(*args, **kwargs)
        class Meta:
            db_table = "payment_to_admin"
        
