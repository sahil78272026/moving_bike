    # admin_id=serializers.CharField(source='user.id')
    # first_name=serializers.CharField(source='user.first_name')
    # last_name=serializers.CharField(source='user.last_name')
    # email=serializers.EmailField(source='user.email')
    # company_name=serializers.CharField()
    # country_code=serializers.CharField(source='user.country_code')
    # mobile=serializers.CharField(source='user.mobile')
    # image=serializers.SerializerMethodField()
    
    # def get_image(self, instance):
    #     if instance.image:
    #         return f'{instance.image.url}' if instance.image else None
    #     return None
from rest_framework import serializers
from customer.models import User
from driverapp.models import TrackerDeviceIntergrations
from adminapp.models import AdminProfile
from superadmin.models import AdminSubscription, TrackerDeviceInfo

class SuperadminLoginSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=[
            "id",
            "first_name",
            "last_name",
            "email",
            "country_code",
            "mobile",
            "image"
            
        ]
    def get_image(self, instance):
        if instance.image:
            return f'{instance.image.url}' if instance.image else None
        return None

class TrackerDeviceIntergrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrackerDeviceIntergrations
        fields=[
            'id',
            'type',
            # 'downlink_type',
            'firmware_version',
            'hardware_version',
            # 'serial_no',
            # 'accelerometer',
            # 'temperature_humidity',
            # 'temperature',
            # 'gps',
            # 'fuel_gauge',
            # 'eeprom',
            # 'pressure',
            # 'ambient_light',
            # 'rfu',
            "device",
            # "data",
            "created_at",
            "updated_at"
        ]
class TrackerListInfoSerializer(serializers.ModelSerializer):
    admin_name =serializers.SerializerMethodField()
    admin_id=serializers.SerializerMethodField()
    class Meta:
        model=TrackerDeviceInfo
        fields=["device","admin_name","admin_id","tracker_availability"]
    def get_admin_name(self, obj):
        admin = obj.admin
        if admin:
            try:
                return AdminProfile.objects.get(user_id=admin.id).company_name
            except AdminProfile.DoesNotExist:
                return None 
        return None
    def get_admin_id(self,obj):
        admin=obj.admin
        if admin:
            return admin.id 
        return None
    
class TrackerListSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrackerDeviceInfo
        fields=['device','tracker_availability']
class AdminSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminSubscription
        fields=['subscription_period','payment_id','sub_start_date','sub_end_date','payment_status','payment_type']

class VendorDetailSerializer(serializers.ModelSerializer):
    mobile=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    class Meta:
        model=AdminProfile
        fields=['company_name','gst','address','mobile','email','pan_number']
    def get_mobile(self,obj):
        admin=obj.user_id 
        if admin:
            admin_obj=User.objects.get(id=admin)
            return admin_obj.mobile 
    def get_email(self,obj):
        admin=obj.user_id 
        if admin:
            try:
                admin_obj=User.objects.get(id=admin)
                return admin_obj.email 
            except:
                pass
        return None


