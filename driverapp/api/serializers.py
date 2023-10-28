from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,RefreshToken
import datetime
from adminapp.models import Truck
from driverapp.models import TrackerDeviceIntergrations,DriverLanguage,Trip,GoogleLatLon
from customer.models import User
from rest_framework import status

from utils.views import post_meridiem_time,post_meridiem_time,post_time,post_meridiem_date,post_24_date_time
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User):
        user.last_login = datetime.datetime.now()
        user.save()
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['userid'] = user.id
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        print(self.user)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': 'Logged in successfully!',
            "driver_id":self.user.id,
            'result': data,
            'additional_data': {},
        }
        return data_payload


from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

class UserSerializer(serializers.ModelSerializer):
    driver_id=serializers.SerializerMethodField()
    truck_id=serializers.SerializerMethodField()
    tracker_id=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['driver_id', 'first_name','last_name','mobile','country_code','email','language_type','truck_id','tracker_id']
        
    def get_driver_id(self,obj):
        return obj.id
    def get_truck_id(self,obj):
        try:
            truck = Truck.objects.filter(driver_id=obj.id).last()
            return truck.id
            if truck is none:
                return None
        except :
            truct=None
            return truct
    def get_tracker_id(self,obj):
        try:
            truck = Truck.objects.filter(driver_id=obj.id).last()
            return truck.tracker_id
        except :
            truct=None
            return truct
        
import json,uuid

# class DriverProfileSerializer(serializers.Serializer):
#     # id =serializers.(source='user.id')
#     first_name=serializers.CharField(source='user.first_name')
    # driver_profile=UserSerializer(required=True,many=False)
    # class Meta:
    #     model=DriverProfile
    #     fields=['driver_profile','image','address','zip_code','city','state']
    

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
    
# class ProfileViewSerializer(serializers.Serializer):
#     id = serializers.UUIDField(format='hex_verbose',source='user.id')
#     first_name=serializers.CharField(source='user.first_name')
#     last_name=serializers.CharField(source='user.last_name')
#     country_code=serializers.CharField(source='user.country_code')
#     mobile=serializers.CharField(source='user.mobile')
#     address=serializers.CharField()
#     city = serializers.CharField(max_length=10)
#     state = serializers.CharField(max_length=10)
#     image = serializers.SerializerMethodField()
#     zip_code=serializers.SerializerMethodField()
#     driving_license=serializers.CharField()
#     language_type=serializers.CharField(source='user.language_type')
    
#     def get_zip_code(self,obj):
#         return obj.pin_code
#     def get_image(self, instance):
#         if instance.image:
#             return f'{instance.image.url}' if instance.image else None
#         return None
    
    
# from drf_extra_fields.fields import Base64ImageField

class DriverProfileSerializer(serializers.ModelSerializer):
    zip_code=serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    # image = Base64ImageField(required=False)
    driving_license=serializers.SerializerMethodField()
    
    class Meta:
        model=User
        fields=[
            'id',
            'first_name',
            'last_name',
            'country_code',
            'mobile',
            'address',
            'city',
            'state',
            'image',
            'zip_code',
            'driving_license',
            'language_type',
        ]
    def get_zip_code(self,obj):
        return str(obj.zipcode)
    def get_image(self, instance):
        if instance.image:
            return f'{instance.image.url}' if instance.image else None
        return None
    def get_driving_license(self,obj):
        return str(obj.driver_license_no)
    
    # def create(self, validated_data):
    #     image=validated_data.pop('image')
    #     # data=validated_data.pop('data')
    #     return User.objects.get_or_create(image=image)
from utils.views import post_meridiem_time

class TrackerDeviceIntergrationAllSerializer(serializers.ModelSerializer):

    timeStamp = serializers.SerializerMethodField()
    # created_at = serializers.SerializerMethodField()
    # updated_at = serializers.SerializerMethodField()

    def get_timeStamp(self, obj):
        return post_24_date_time(obj.timeStamp)
    
    # def get_created_at(self, obj):
    #     return  post_meridiem_date(obj.created_at)
    
    # def get_updated_at(self, obj):
    #     return post_meridiem_date(obj.updated_at)

    class Meta:
        model=TrackerDeviceIntergrations
        fields=[
                "status",
                "admin",
                "tracker_availability",
                "device",
                "data",
                "type",
                "downlink_type",
                "firmware_version",
                "hardware_version",
                "serial_no",
                "accelerometer",
                "temperature_humidity",
                "temperature_value",
                "gps",
                "fuel_gauge",
                "eeprom",
                "pressure",
                "ambient_light",
                "rfu",
                "battery_level",
                "temperature_sign",
                "temperature",
                "humidity",
                "motion_sensor",
                "position",
                "roll_angle",
                "pitch_angle",
                "lat_degree",
                "lat_min1",
                "lat_min2",
                "lat_min3",
                "lon_degree",
                "lon_min2",
                "latitude",
                "longitude",
                "mac_time",
                "alerttype",
                "tilt",
                "fall_detection",
                "theft",
                "low_battery_level",
                "alert_temperature",
                "alert_humidity",
                "old_position",
                "new_position",
                "seqNumber",
                "timeStamp",
                "created_at",
                "updated_at",   
                ]
    

class  TrackerDeviceIntergrationAllDetailSerializer(serializers.ModelSerializer): 
    class Meta:
        model=TrackerDeviceIntergrations
        fields='__all__'
        
class TrackerDeviceIntergrationAlertSerializer(serializers.ModelSerializer):
    alert_battery_level=serializers.SerializerMethodField()
    alert_motion_sensor=serializers.SerializerMethodField()
    alert_theft=serializers.SerializerMethodField()
    alert_position=serializers.SerializerMethodField()
    alert_new_position=serializers.SerializerMethodField()
    alert_temperature_sign=serializers.SerializerMethodField()
    alert_temperature=serializers.SerializerMethodField()
    alert_humidity=serializers.SerializerMethodField()
    class Meta:
        model=TrackerDeviceIntergrations
        fields=[
            'id',
            'type',
            'device',
            'alerttype',
            'alert_battery_level',
            'alert_motion_sensor',
            "alert_theft",
            'mac_time',
            "alert_position",
            'alert_new_position',
            "alert_temperature_sign",
            "alert_temperature",
            'alert_humidity',
            'created_at',
            'updated_at'
        ]
    def get_alert_battery_level(self,obj):
        if obj.battery_level is not None:
            data=obj.battery_level
        else:
            data=""
        return data
    def get_alert_motion_sensor(self,obj):
        if obj.motion_sensor is not None:
            data=obj.motion_sensor
        else:
            data=""
        return data
    def get_alert_theft(self,obj):
        if obj.theft is not None:
            data=obj.theft
        else:
            data=""
        return data
    def get_alert_theft(self,obj):
        if obj.theft is not None:
            data=obj.theft
        else:
            data=""
        return data
    def get_alert_position(self,obj):
        if obj.position is not None:
            data=obj.position
        else:
            data=""
        return data
    def get_alert_new_position(self,obj):
        if obj.new_position is not None:
            data=obj.new_position
        else:
            data=""
        return data
    def get_alert_temperature_sign(self,obj):
        if obj.temperature_sign is not None:
            data=obj.temperature_sign
        else:
            data=""
        return data
    def get_alert_temperature(self,obj):
        if obj.temperature is not None:
            data=obj.temperature
        else:
            data=""
        return data
    def get_alert_humidity(self,obj):
        if obj.humidity is not None:
            data=obj.humidity
        else:
            data=""
        return data
    
    
class TrackerDeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrackerDeviceIntergrations
        fields=['device']

    
class TrackerDeviceIntergrationSerializer(serializers.ModelSerializer):
    # timeStamp=serializers.SerializerMethodField()
    class Meta:
        model=TrackerDeviceIntergrations
        fields=[
            'id',
            'type',
            'downlink_type',
            'firmware_version',
            'hardware_version',
            'serial_no',
            'accelerometer',
            'temperature_humidity',
            'temperature',
            'gps',
            'fuel_gauge',
            'eeprom',
            'pressure',
            'ambient_light',
            'rfu',
            "device",
            "data",
            'timeStamp',
            "created_at",
            "updated_at",
            "seqNumber"
        ]
    # def get_timeStamp(self,obj):
    #     return post_meridiem_time(obj.timeStamp)

        
        
class DriverLanguageSerialiser(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    class Meta:
        model=DriverLanguage
        fields=['id',"name"]
        
    def get_id(self,obj):
        return str(obj.id)
    
class FeebbackTripSerializer(serializers.ModelSerializer):
    trip_id=serializers.SerializerMethodField()
    rating=serializers.SerializerMethodField()
    class Meta:
        model=Trip 
        fields=('feedback','issue','trip_id','rating','trip_id_show')
    def get_trip_id(self,obj):
        return str(obj.id)
    def get_rating(self,obj):
        if obj.rating==None:
            data=0
        else:
            data=round(obj.rating)
        return data


class GoogleTripTrackerLatLongSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoogleLatLon
        fields='__all__'