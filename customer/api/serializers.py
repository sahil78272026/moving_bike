from rest_framework import serializers
from customer.models import Coupon,Organization,Material,MaterialSubtype,FirePushNotication,User
from driverapp.models import TrackerDeviceIntergrations
from adminapp.models import Truck, Trip, AdminResponse

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ('id', 'type')

class TruckSerializer_vendor(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ('id', 'type', 'vendor_name')

class Coupon_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class TruckIDWithTrackerIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields =['user','truck_no','tracker_id']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields='__all__'
        # fields=[
        #     'id',
        #     "user",
        #     'name',
        #     'organization_name',
        #     'gst',
        #     'pan',
        # ]
class Trackerdeviceintegrations(serializers.ModelSerializer):
    class Meta:
        model=TrackerDeviceIntergrations
        fields='__all__'
        
class SubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=MaterialSubtype
        fields='__all__'
class MaterialSerializer(serializers.ModelSerializer):
    subtypes = SubTypeSerializer(many=True, read_only=True)
    class Meta:
        model=Material
        fields=['id','material_type','subtypes']
    
class GetQuoteSerializer(serializers.ModelSerializer):
    constraints=SubTypeSerializer()
    material_type=serializers.CharField(allow_blank=True)
    material_weight=serializers.CharField(allow_blank=True)
    material_subtype=serializers.CharField(allow_blank=True)
    class Meta:
        model=Trip
        fields='__all__'
    def create(self, validated_data):
        print(validated_data)
        data = validated_data.copy()
        material_subtype=validated_data.pop('material_subtype')
        material_type=validated_data.pop('material_type')
        material_weight=validated_data.pop('material_weight')
        constraints = validated_data.pop('constraints')
        material_instance=Material.objects.create(material_type=material_type)
        subtype_instance = MaterialSubtype.objects.create(material=material_instance,material_weight=material_weight,material_subtype=material_subtype,**constraints)
        trip = Trip.objects.create(submaterial=subtype_instance,material=material_instance,**validated_data)
        return data
    
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trip
        fields=['starting_point','destination','submaterial','material','truck_type','trip_status']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=FirePushNotication
        fields=['title','description']
class UpdateProfileSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(source='profile.image')
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    
    class Meta:
        model=User
        fields=['first_name','last_name','email','mobile','image']

    def get_first_name(self, obj):
        if obj.first_name is None:
            return ''
        else: return obj.first_name
    
    def get_last_name(self, obj):
        if obj.last_name is None:
            return ''
        else: return obj.last_name
    
    def get_email(self, obj):
        if obj.email is None:
            return ''
        else: return obj.email

    def get_image(self, obj):
        return obj.image.url
        


class ViewaddressbookSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['address','village','city','state','zipcode', 'country']


class ViewvendorlistSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminResponse
        fields='__all__'

class UpdateKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','kyc_numer','kyc_file']

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Trip
        fields=['id','amount_paid','payment_date','payment_status', 'razorpay_payment_id', 'razorpay_order_id','payment_issue']


class Coupon_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['coupon_code','coupon_amt']