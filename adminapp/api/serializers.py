from rest_framework import serializers
from customer.models import User
from adminapp.models import AdminProfile,Truck,AddDriver,AdminTripDetails,Trip
from driverapp.models import TrackerDeviceIntergrations
from utils.views import post_meridiem_date
class AdminSerializer(serializers.Serializer):
    admin_id=serializers.CharField(source='user.id')
    first_name=serializers.CharField(source='user.first_name')
    last_name=serializers.CharField(source='user.last_name')
    email=serializers.EmailField(source='user.email')
    company_name=serializers.CharField()
    country_code=serializers.CharField(source='user.country_code')
    mobile=serializers.CharField(source='user.mobile')
    image=serializers.SerializerMethodField()
    
    def get_image(self, instance):
        if instance.image:
            return f'{instance.image.url}' if instance.image else None
        return None
    
class FleetViewSerializer(serializers.ModelSerializer):
    driver_name=serializers.SerializerMethodField()
    supervisor_name=serializers.SerializerMethodField()
    truck_id=serializers.SerializerMethodField()
    class Meta:
        model=Truck
        fields=['truck_id','chassis_no','type','capacity','tyre_count','truck_no','manufacturer','container_no','registration_date','rc_expiry','avail_status',
                'pollution_certificate','rc','width','pollution_expiry','height','tracker_id','driver_id','driver_name','supervisor_id','supervisor_name','tracker_id']
    def get_driver_name(self,obj):
        driver_instance=obj.driver
        if driver_instance is None:
            return None
        else:
            return obj.driver.first_name
    def get_truck_id(self,obj):
        truck_instance=obj.id
        return truck_instance
    def get_supervisor_name(self,instance):
        supervisor=instance.supervisor
        if supervisor is None:
            return None
        else:
            return instance.supervisor.first_name
class VechicleTruckSerializer(serializers.ModelSerializer):
    truck_id=serializers.SerializerMethodField()
    class Meta:
        model=Truck
        fields=['truck_id','truck_no']
    def get_truck_id(self,obj):
        truck_instance=obj.id
        return truck_instance
class DriverGetSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields=['first_name','last_name']
        
class AdminAddDeriverSerializer(serializers.ModelSerializer):
    driver=DriverGetSerializer(many=True,read_only=True)

    class Meta:
        model=AddDriver
        fields=['driver']
        # fields=[
        #     'first_name',
        #     'last_name',
        #     'mobile',
        #     'country_code',
        #     'address',
            # 'city',
            # 'city',
            # 'state',
            # 'zipcode',
            # 'one_time_password',
            # 'driver_license_no',
        # ]
    # def get_first_name(self,obj):
    #     return  str(obj.driver.first_name)
    
    # def get_last_name(self,obj):
    #     return  str(obj.driver.last_name)
    # def get_mobile(self,obj):
    #     return  str(obj.driver.mobile)
    # def get_country_code(self,obj):
    #     return  str(obj.country_code)
    # def get_address(self,obj):
    #     return  str(obj.address)
        
        
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['driver'] = DriverGetSerializer(instance.driver).data
    #     return response
    
# class AdminTripSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Trip
#         fields=['destination','starting_point','truck_type','starting_time']
class PaymentStatusSerializer(serializers.ModelSerializer):
    trip_id=serializers.SerializerMethodField()
    class Meta:
        model=Trip
        fields=['trip_id','trip_id_show','payment_status','trip_status','razorpay_payment_id','starting_point','destination','starting_date','amount']
    def get_trip_id(self,obj):
        trip_instance=obj.id
        if trip_instance is None:
            return None
        else:
            return trip_instance
        
        
class TrackerDeviceIntergrationsAdminLocationSerializer(serializers.ModelSerializer):
    timeStamp=serializers.SerializerMethodField()
    class Meta:
        model=TrackerDeviceIntergrations
        fields=(
            'id',
            'latitude',
            'longitude',
            "device",
            "address",
            "timeStamp"
        )
    def get_timeStamp(self,obj):
        return post_meridiem_date(obj.timeStamp)

class TrackerDeviceIntergrationsAdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrackerDeviceIntergrations
        fields=(
            'id',
            'latitude',
            'longitude',
            "device",
        )

class TripOngoingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trip
        fields=(
            'id',
            'starting_point',
            'destination',
            'trip_status',
            
        )
class AllTripOngoingSerializer(serializers.ModelSerializer):
    trip_id=serializers.SerializerMethodField()
    truck_no=serializers.SerializerMethodField()
    truck_id=  serializers.SerializerMethodField()
    class Meta:
        model=Trip
        fields=(
            'trip_id',
            'trip_status',
            "truck_id",
            "truck_no"
            
        )
    def get_trip_id(self,obj):
        return obj.id
    def get_truck_id(self,obj):
        return obj.truck.id
    def get_truck_no(self,obj):
        return obj.truck.truck_no

class AllTrackerDeviceIntergrationsAdminLocationSerializer(serializers.ModelSerializer):
    trip=AllTripOngoingSerializer(many=True)
    class Meta:
        model=TrackerDeviceIntergrations
        fields=(
            'id',
            'latitude',
            'longitude',
            "device",
    
        )