from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils.text import slugify
import string, random
import datetime
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.fields import JSONField
import json,uuid
from customer.custom_azure import AzureMediaStorage as AMS


class UserManager(BaseUserManager):
    """ This is model manager for customized user which uses email field as default username field."""

    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """This method creates and saves new user through email and password."""
        if not email:
            raise ValueError('Email is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """This method creates and saves regular users using email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """This method creates and save SuperUser using email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# custom user model
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Prefer not to answer', 'Prefer not to answer'),
]

MARITAL_STATUS_CHOICES = [
    ('Married', 'Married'),
    ('Unmarried', 'Unmarried'),
    ('Prefer not to answer', 'Prefer not to answer'),
]


class User(AbstractUser):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    """Custom User model to use email as default ."""
    username = models.CharField(max_length=400,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    mobile=models.CharField(max_length=20,null=True,blank=True)
    country_code = models.CharField(max_length=5,null=True,blank=True)
    email_verified = models.BooleanField(default=False)
    otp=models.CharField(max_length=4,null=True,blank=True)
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES, default='Prefer not to answer', null=True,
                              blank=True)
    nationality = models.CharField(max_length=20, default='Indian', null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True, null=True, blank=True, )
    last_modified_on = models.DateTimeField(null=True, blank=True, auto_now=True )
    changed_password_on = models.DateTimeField(blank=True, null=True)
    verified= models.BooleanField(default=False,null=True,blank=True)
    marital_status = models.CharField(max_length=25, choices=MARITAL_STATUS_CHOICES, default='Prefer not to answer')
    slug = models.SlugField(null=True, blank=True, max_length=100)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    one_time_pwd=models.CharField(max_length=20,null=True,blank=True)
    role_staff_type = (

        ('customer', 'customer'),
        ('user', 'user')  ,
        ('admin', 'admin'),
        ('supervisor','supervisor'),
        ('superadmin', 'superadmin'),
        ('driver', 'driver')

    )
    role = models.CharField(max_length=14, choices=role_staff_type,null=True,blank=True)
    customer_type = (

        ('Organization', 'Organization'),
        ('Individual', 'Individual')

    )
    driver_status_choices = (
        ('On trip', 'On trip'),
        ('Available', 'Available')
    )

    type = models.CharField(max_length=14, choices=customer_type,null=True,blank=True)
    kyc_numer=models.CharField(max_length=300,null=True,blank=True)
    kyc_file = models.ImageField(upload_to='KYC/',  null=True, blank=True)
    kyc_verified= models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True )
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    fcm_token=models.CharField(max_length=500,null=True,blank=True,default='fowFBvaYQ7S-dBwb30tOxq:APA91bFQq6YNHF8CzHlrArecgrBTfXJhLjIPyZbKPZzdpapZ5ePWH0hgbaTpFEUY0MfioavhHqZQF15k7O8yeXGHiD92o3Pv4YXZH9gwdD61m9pbw6YtpUaEAlpjy7Pd-cJWnggfV5SM')
    truck_no=models.CharField(max_length=500,null=True,blank=True)
    tracker_id=models.CharField(max_length=500,null=True,blank=True)
    language_type=models.CharField(max_length=100,null=True,blank=True,default="English")
    coupon_code=models.CharField(max_length=50,null=True,blank=True)
    subscription=models.FloatField(null=True,blank=True,default='1.0')
    #------------------
    image = models.ImageField(upload_to='profile_pictures/',default='profile_pictures/default.png',storage=AMS, null=True, blank=True)
    gst=models.CharField(max_length=255,null=True,blank=True)
    pan_number=models.CharField(max_length=10,null=True,blank=True)
    company_name=models.CharField(max_length=255,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    resedential_proof=models.ImageField(upload_to='admin_documents/',storage=AMS,null=True,blank=True)
    village=models.CharField(max_length=500,null=True,blank=True)
    city=models.CharField(max_length=500,null=True,blank=True)
    state=models.CharField(max_length=500,null=True,blank=True)
    zipcode=models.CharField(max_length=6,null=True,blank=True)
    country=models.CharField(max_length=20,null=True,blank=True)
    driver_license_no=models.CharField(max_length=100,null=True,blank=True)
    driver_status=models.CharField(choices=driver_status_choices,max_length=50,null=True,blank=True)
    is_deleted=models.BooleanField(default=False,null=True,blank=True)
    resedential_proof=models.ImageField(upload_to='admin_documents/',storage=AMS,null=True,blank=True,default='profile_pictures/default.png')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True )
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)
    issue=models.TextField(null=True,blank=True)
    priority_number = models.IntegerField(null=True,blank=True)
    priority_status = models.BooleanField(default=False)




    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.id)

    # def __unicode__(self):
    #     return str(self.id)



    class Meta:

        verbose_name_plural = "Users"
        db_table = "generic_user"




def unique_slug_generator(instance):
    if not instance.first_name:
        return None
    if not instance.last_name:
        last_name = 'identifier'

    constant_slug = slugify(' '.join([instance.first_name, instance.last_name or last_name, '#']))
    slug = constant_slug
    Klass = instance.__class__
    random_number = random.randint(2, 4)
    while Klass.objects.filter(slug=slug).exists():
        str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(random_number))
        slug = "{slug}.{str}".format(slug=constant_slug, str=str)
    return slug + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))


@receiver(pre_save, sender=User)
def get_slug(sender, instance, *args, **kwargs):
    if instance.pk is None:
        instance.slug = unique_slug_generator(instance)


#https://trackerfilestore.blob.core.windows.net/trackerbackendimage/trackerfilestore.blob.core.windows.net/profile_pictures/default.png

class Coupon(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    COUPON_TYPE = (

        ('common', 'common'),
        ('specific', 'specific'),
    )
    coupon_code=models.CharField(max_length=100,null=True,blank=True, unique=True)
    coupon_amt=models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=25, choices=COUPON_TYPE, default=None, null=True,
                              blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    percent_discount = models.IntegerField(blank=True, null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    # country_code = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.coupon_code)

    class Meta:
        db_table = "coupon"


class Profile(models.Model):
    """Profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    alternate_phone = models.CharField(max_length=10, null=True, validators=[RegexValidator(r'^\d{3}\d{3}\d{4}$')])
    image = models.ImageField(upload_to='profile_pictures/',storage=AMS, null=True, blank=True)
    slug = models.SlugField(blank=True, max_length=150)
    address = models.TextField(null=True, blank=True, )
    pin_code = models.CharField(max_length=6,
                                blank=True,
                                null=True,
                                )
    city = models.CharField(max_length=50,
                            null=True,
                            blank=True,
                            )
    course = models.CharField(max_length=50,
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
    class Meta:
        db_table = "customer_profile"


class MobileOTP(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    # mobile = PhoneNumberField(blank=True,null=True,unique=True)
    mobile=models.CharField(max_length=20,null=True,blank=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    time=models.CharField(max_length=50,null=True,blank=True)
    count = models.IntegerField(default=0, help_text = 'Number of opt_sent')
    validated = models.BooleanField(default=False, help_text= 'if it is true, that means user have validate opt correctly in seconds')
    otp_verify=models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.mobile)
    class Meta:
        db_table = "mobileotp"
    # + ' is sent ' + str(self.otp) +'time in date ' +str(self.time)
class Organization(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Organization',null=True,blank=True)
    name=models.CharField(max_length=254, blank=True, null=True)
    organization_name=models.CharField(max_length=254, blank=True, null=True)
    gst=models.CharField(max_length=15, blank=True, null=True)
    pan=models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type = "Organization"
        super().save(*args, **kwargs)

    class Meta:
        db_table = "organization"


class Material(models.Model):
    id=models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    material_type=models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = "material"

class MaterialSubtype(models.Model):
    id=models.UUIDField(primary_key= True,default= uuid.uuid4,editable= False)
    material=models.ForeignKey(Material,default=None,on_delete=models.CASCADE)
    material_subtype=models.CharField(max_length=50,null=True)
    material_type=models.CharField(max_length=100,null=True,blank=True,default='short lived')
    material_weight = models.CharField(max_length=100,null=True,blank=True)
    temprature=models.CharField(max_length=100,null=True,blank=True)
    humidity=models.CharField(max_length=100,null=True,blank=True)
    tilt=models.CharField(max_length=100,null=True,blank=True,default=False)
    ambient_light=models.CharField(max_length=100,null=True,blank=True)
    pitch_angle=models.CharField(max_length=100,null=True,blank=True)
    roll_angle=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = "materialsubtype"


fire_choice = [
    ('1', '1'),#customer
    ('2', '2'),#driver
    ('3', '3'),#admin
]

class FirePushNotication(models.Model):
    title=models.CharField(max_length=100,null=True,blank=True)
    description=models.CharField(max_length=100,null=True,blank=True)
    status=models.BooleanField(default=True,blank=True,null=True)
    fire_type = models.CharField(max_length=25, choices=fire_choice, default=None, null=True,
                              blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True,)
    updated_at = models.DateTimeField(auto_now=True,null=True,
                                      blank=True,)
    role=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return str(self.title)
    class Meta:
        db_table = "firepushnotication"



# class Photo(models.Model):
#     image_file = models.ImageField(upload_to='profile_pictures', storage=AMS, null=True, blank=True )

