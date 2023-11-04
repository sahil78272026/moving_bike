from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from driverapp.api.renders import UserRenderer,UserTokenRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from driverapp.api.serializers import MyTokenObtainPairSerializer,LoginSerializer,UserSerializer,DriverProfileSerializer,\
    TrackerDeviceIntergrationSerializer,TrackerDeviceIntergrationAllSerializer,TrackerDeviceInfoSerializer,DriverLanguageSerialiser,\
    TrackerDeviceIntergrationAlertSerializer,DriverProfileSerializer,TrackerDeviceIntergrationAllDetailSerializer,FeebbackTripSerializer,GoogleTripTrackerLatLongSerializer
from rest_framework import status
from driverapp.models import TrackerDeviceIntergrations, DriverLanguage,GoogleLatLon
from customer.models import User,MobileOTP
from customer.api.sendmobileotp import send_otp
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.parsers import FormParser,MultiPartParser
import requests,json
from rest_framework import pagination
from driverapp.api.tracker_decryt import *
from rest_framework.pagination import PageNumberPagination
from customer.models import FirePushNotication
from customer.api.serializers import TruckIDWithTrackerIDSerializer
from datetime import datetime,timedelta
from adminapp.models import AddDriver, Truck, Trip
from customer.api.sendmobileotp import send_otp
from customer.api.views import send_notification
from driverapp.api.tracker_decryt import googleLatLon
from driverapp.api.base64 import base64_file
from utils.views import post_meridiem_time,post_meridiem_date
from superadmin.models import TrackerDeviceInfo

class PagePagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_size = 10

class DriverappView(viewsets.ViewSet):
    def list(self, request):
        return Response({"message":"driver app"})

# class DriverAddView(viewsets.ViewSet):
#     def create(self, request):
#         mobile = request.data.get('mobile')
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         country_code = request.data.get('country_code')
#         type = request.data.get('type')
#         error_object = {}
#         error_flag = False
#         if not mobile:
#             error_object['mobile'] = "Mobile not provided"
#             error_flag = True
#         if not country_code:
#             error_object['country_code'] = "Country code not provided"
#             error_flag = True
#         if not first_name:
#             error_object['first_name'] = "First Name not provided"
#             error_flag = True
#         if not last_name:
#             error_object['last_name'] = "Last Name not provided"
#             error_flag = True
#         if error_flag:
#             response_payload = {
#                 'is_authenticated': False,
#                 'status':status.HTTP_400_BAD_REQUEST,
#                 'messages': error_object,
#                 'result': 'otp not created',
#                 'additional_data': {},
#             }

#             return Response(response_payload)
#         user_object,created = User.objects.get_or_create(mobile=mobile)
#         user_object.country_code=country_code
#         user_object.type=type
#         user_object.mobile=mobile
#         user_object.save()
#         profile, created = DriverProfile.objects.get_or_create(user=user_object)
#         profile.save()
#         user_object.save()
#         otp_object,created =MobileOTP.objects.get_or_create(user=user_object)
#         otp_object.mobile=mobile
#         otp_object.otp=send_otp(mobile,country_code)["otp"]  
#         otp_object.time=int(float((datetime.now().timestamp())))
#         otp_object.save()
#         response_payload = {
#             'is_authenticated': True,
#             'status': status.HTTP_201_CREATED,
#             "mobile_no":str(user_object.mobile),
#             'messages': 'OTP send succesfully on your registared mobile number',
#            "result": {},
#             'additional_data': {},
#         }
#         return Response(response_payload)


class LoginViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    print("ok")
    def create(self, request, *args, **kwargs):
        email=request.data.get('email')
        password=request.data.get('password')
        error_object={}
        #error_flag=False
        if not email:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Email is not provided',
               "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        if not password:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'password not provided',
               "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        
        try:
            user=User.objects.get(email=email)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "email id is not valid",
               "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'password is not valid',
                'result':{},
                'additional_data': {},
            }

            return Response(response_payload)
        response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_200_OK,
                'messages':'Driver login successfull',
                'result':serializer.validated_data,
                'additional_data': {},
            }

        return Response(response_payload)

class DriverLoginView(viewsets.ViewSet):
    
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    def create(self, request):
        # try:
        password = request.data.get('password')
        mobile = request.data.get('mobile')
        fcm_token = request.data.get('fcm_token')
        if not password:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Password is not provided',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Mobile is not provided',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        
        try:
            user = User.objects.get(mobile=mobile, role='driver')
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Mobile number not valid',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        refresh_token=RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        refresh_token = str(refresh_token)     
    
        if  user.one_time_pwd==password:
            
            login_serializer=UserSerializer(user)
            login_data=login_serializer.data
            User.objects.filter(mobile=mobile, role='driver').update(fcm_token=fcm_token)

            data={}
            data['access_token']=access_token
            data['refresh_token']=refresh_token
            response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                "messages":"Login Successful",
                "result":{}, 
                'additional_data': {},
            }
            response_payload.update(login_data)
            response_payload.update(data)

            return Response(response_payload)
        
        else:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Please enter valid Password',
                "result":{}, 
                'additional_data': {},
            }

            return Response(response_payload)
        # except Exception as e:
        #     response_payload = {
        #                 'is_authenticated': True,
        #                 'status':500,
        #                 "messages":"server error ",
        #                 "result":{},
        #                 'additional_data': {},
        #             }
        #     return Response(response_payload)
        



  

 
class PersonalInformationImageView(generics.GenericAPIView):
    # parser_classes = [MultiPartParser, FormParser]
    queryset = User.objects.all()
    serializer_class = DriverProfileSerializer
    # renderer_classes=[UserRenderer]
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        image = request.data.get('image')
        if not image:
            response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': 'image is not provided',
               "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        try:
            user = User.objects.get(id=str(request.user),role='driver')
        except:
            response_payload = {
                'is_authenticated':False ,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': 'User does not exist',
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        user.image=base64_file(image)
        user.save()
        serializer = DriverProfileSerializer(user)
        data = serializer.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages':"Driver update profile image successfull",
            'result': data,
            'additional_data': {},
        }
        return Response(response_payload)
    
class PersonalInformationEditView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = DriverProfileSerializer
    # renderer_classes=[UserRenderer]
    permission_classes = (IsAuthenticated,)
    def get(self, request):        
        try:
            user = User.objects.get(id=str(request.user),role='driver')
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Driver id not valid please provided valid id',
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        serializer = DriverProfileSerializer(user)
        data = serializer.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "Driver fetch details successfull",
            'result': data,
            'additional_data': {},
        }
        return Response(response_payload)


    def post(self, request, *args, **kwargs):
        user_slug = request.GET.get('id')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        # image = request.data.get('image')
        mobile = request.data.get('mobile')
        country_code = request.data.get('country_code')
        gender = request.data.get('gender')
        address = request.data.get('address')
        landmark = request.data.get('landmark')  #
        pincode = request.data.get('zip_code')
        date_of_birth = request.data.get('date_of_birth') or None
        state = request.data.get('state')
        city = request.data.get('city')
        driving_license = request.data.get('driving_license')
        error_object={}
        error_flag=False
                
        if not mobile:
            error_object['mobile'] = "phone number is not provided"
            error_flag = True
        
        try:
            # user = User.objects.get(id=user_slug)
            user = User.objects.get(id=str(request.user),role='driver')
        except:
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': 'User does not exist',
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)

        
        if error_flag:
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': '',
                'result': error_object,
                'additional_data': {},
            }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)

        
        user.mobile=mobile
        user.gender=gender    
        user.first_name=first_name
        user.last_name=last_name
        user.country_code=country_code
        user.pin_code = pincode
        user.state = state
        user.city = city  
        user.address=address    
        user.landmark = landmark
        user.driver_license_no=driving_license
        user.date_of_birth=date_of_birth
        user.save()
        serializer=DriverProfileSerializer(user)
        data = serializer.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages':"Driver update detail successfull",
            'result': data,
            'additional_data': {},
        }
        return Response(response_payload, status=status.HTTP_200_OK)
    

    
class CallBackURL(generics.GenericAPIView):
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAllSerializer
    
    permission_classes = (AllowAny,)
    def get(self, request):
        queryset_data = TrackerDeviceIntergrations.objects.all().order_by('created_at').order_by("-id")

        serializer = self.get_serializer(queryset_data,many=True)
        pay_load=serializer.data
        
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "",
            'result': pay_load,

            'additional_data': {},
        }
        return Response(response_payload)
    
    

class CallBackURLDetailView(generics.GenericAPIView,PageNumberPagination):
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAllSerializer
    pagination_class = PagePagination
   
    def get(self, request, slug=None):
            
        queryset = TrackerDeviceIntergrations.objects.filter(device=slug).order_by('-id')
        serializer = TrackerDeviceIntergrationAllSerializer(queryset, many=True)
        pay_load=serializer.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "",
            'result': pay_load,
            'additional_data': {},
        }
        return Response(response_payload)
       
            
class DeviceAlertView(generics.GenericAPIView):
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAlertSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        deviceid=request.GET.get('deviceid')
        if not deviceid:
            response_payload = {
            'is_authenticated': False,
            'status':status.HTTP_400_BAD_REQUEST,
            'messages': "Get method is not allowed",
            "result": {},
            'additional_data': {},
           }
            return Response(response_payload)
        try:
            queryset = TrackerDeviceIntergrations.objects.filter(device=deviceid.upper(),type='Alert Data').order_by('-id').first()
        except Exception as e:
            response_payload = {
            'is_authenticated': False,
            'status':status.HTTP_400_BAD_REQUEST,
            'messages': "Tracker id does not exist",
            "result": {},
            'additional_data': {},
            }
            return Response(response_payload)     
        if queryset is not None:
            
            serializer = TrackerDeviceIntergrationAlertSerializer(queryset)
            pay_load=serializer.data
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': "Alert data successfully",
                'result': pay_load,
                'additional_data': {},
            }
            return Response(response_payload)
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Invalid tracker id",
                   "result": {},
                    'additional_data': {},
                    }
            return Response(response_payload)
        
class GoogleTripTrackerLatLongView(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def list(self,request):
        id=request.user.id
        trip_id=request.data.get('trip_id')
        glat=request.data.get('glat')
        glon=request.data.get('glon')
        if not glat:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "Please enter google google latitude value",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        if not glon:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "Please enter google goole longitude value",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        try:
            user_obj=User.objects.get(id=id)
        except:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "User does not exist",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        # print('user_id',user_id,id)
        try:
            trip_obj=Trip.objects.get(id=trip_id)
        except:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "Trip does not exist",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        queryset=GoogleLatLon.objects.filter(trip=trip_obj.id,driver=user_obj.id)
        google_serializer=GoogleTripTrackerLatLongSerializer(queryset,many=True)
        pay_load=google_serializer.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "Alert data successfully",
            'result': pay_load,
            'additional_data': {},
        }
        return Response(response_payload)
    def create(self, request):
        id=request.user.id
        trip_id=request.data.get('trip_id')
        glat=request.data.get('glat')
        glon=request.data.get('glon')
        if not glat:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "Please enter google google latitude value",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        if not glon:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "Please enter google goole longitude value",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        try:
            user_obj=User.objects.get(id=id)
        except:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "User does not exist",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        # print('user_id',user_id,id)
        try:
            trip_obj=Trip.objects.get(id=trip_id)
        except:
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': "Trip does not exist",
            'result': {},
            'additional_data': {},
            }
            return Response(response_payload)
        print('trip_id',trip_obj)
        address_data=googleLatLon(glat,glon)
        google_obj=GoogleLatLon()
        google_obj.driver_id=user_obj.id
        google_obj.trip_id=trip_obj.id
        google_obj.glat=glat
        google_obj.glon=glon
        google_obj.address=address_data
        google_obj.save()
        google_serializer=GoogleTripTrackerLatLongSerializer(google_obj)
        pay_load=google_serializer.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "Alert data successfully",
            'result': pay_load,
            'additional_data': {},
        }
        return Response(response_payload)
        

            

    
class TrackerCallBackURL(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def list(self,request):
        queryset = TrackerDeviceIntergrations.objects.filter(type='Device Information',status=True).distinct('device')[::-1]
        # queryset = TrackerDeviceIntergrations.objects.filter(type='Device Information',status=True).order_by("-id")
        serializer_data = TrackerDeviceIntergrationSerializer(queryset,many=True)
        pay_load=serializer_data.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "",
            'result': pay_load,
            'additional_data': {},
        }
        return Response(response_payload)
    
    def create(self, request):
        type=request.data.get('type')
        battery_level=request.data.get('battery_level')
        temperature=request.data.get('temperature')
        sensor_data=request.data.get('sensor_data')
        position_data=request.data.get('position_data')
        roll_angle=request.data.get('roll_angle')
        pitch_angle=request.data.get('pitch_angle')
        mac_time=request.data.get('mac_time')
        device=request.data.get('device')
        trip_id=request.data.get('trip_id')
        
        seqNumber = request.data.get("seqNumber") or 123
        timeStamp = request.data.get("timeStamp") or  "2023-10-05 09:22:54"
        data=request.data.get('data')
    
        # def timeStamp_value_converted(value):
        #     if value == "RealTime":
        #         data = timeStamp
        #     else:
        #         value = int(value)
        #         timestamp_datetime = datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")
        #         new_datetime = timestamp_datetime - timedelta(seconds=value)
        #         data = new_datetime.strftime("%Y-%m-%d %H:%M:%S.%f %z")
        #     return data
        
        if data[:2]=='01':
            tracker_decrypted_obj=tracker_dcryted_payload_01(data)
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_device_obj.firmware_version=tracker_decrypted_obj['firmware_version']
            tracker_device_obj.hardware_version=tracker_decrypted_obj['hardware_version']
            tracker_device_obj.serial_no=tracker_decrypted_obj['serial_no']
            tracker_device_obj.accelerometer=tracker_decrypted_obj['accelerometer']
            tracker_device_obj.temperature_humidity=tracker_decrypted_obj['temperature_humidity']
            tracker_device_obj.temperature_value=tracker_decrypted_obj['temperature']
            tracker_device_obj.gps=tracker_decrypted_obj['gps']
            tracker_device_obj.fuel_gauge=tracker_decrypted_obj['fuel_gauge']
            tracker_device_obj.eeprom=tracker_decrypted_obj['eeprom']
            tracker_device_obj.pressure=tracker_decrypted_obj['pressure']
            tracker_device_obj.ambient_light=tracker_decrypted_obj['ambient_light']
            tracker_device_obj.rfu=tracker_decrypted_obj['rfu']
            tracker_device_obj.type=tracker_decrypted_obj['type']
            tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data.
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
            
        if data[:2]=='02' or data[:2]=='22' or data[:2]=='20':
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_decrypted_obj=tracker_dcryted_payload_02(data)
            tracker_device_obj.type=tracker_decrypted_obj['type']
            tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
            tracker_device_obj.battery_level=tracker_decrypted_obj['battery_level']
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
        elif data[:2]=='03' or data[:2]=='30' or data[:2]=='33':
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_decrypted_obj=tracker_dcryted_payload_03(data)
            tracker_device_obj.type=tracker_decrypted_obj['type']
            tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
            tracker_device_obj.battery_level=tracker_decrypted_obj['battery_level']
            tracker_device_obj.temperature=tracker_decrypted_obj['temperature']
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
           
        elif data[:2]=='04':
            tracker_decrypted_obj=tracker_dcryted_payload_04(data)
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_device_obj.type=tracker_decrypted_obj['type']
            tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
            tracker_device_obj.battery_level=tracker_decrypted_obj['battery_level']
            tracker_device_obj.temperature=tracker_decrypted_obj['temperature']
            tracker_device_obj.humidity=tracker_decrypted_obj['humidity']
            tracker_device_obj.motion_sensor=tracker_decrypted_obj['motion_sensor']
            tracker_device_obj.position=tracker_decrypted_obj['position']
            tracker_device_obj.roll_angle=tracker_decrypted_obj['roll_angle']
            tracker_device_obj.pitch_angle=tracker_decrypted_obj['pitch_angle']
            tracker_device_obj.mac_time=tracker_decrypted_obj['mac_time']
            tracker_device_obj.temperature_sign=tracker_decrypted_obj['temperature_sign']
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
        elif data[:3]=='004' or data[:4]=='0004':
            if data[5:][:2]=="04" :
                tracker_decrypted_obj=tracker_dcryted_payload_04_duplicate(data[5:])
                tracker_device_obj=TrackerDeviceIntergrations()
                tracker_device_obj.type=tracker_decrypted_obj['type']
                tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
                tracker_device_obj.battery_level=tracker_decrypted_obj['battery_level']
                tracker_device_obj.temperature=tracker_decrypted_obj['temperature']
                tracker_device_obj.humidity=tracker_decrypted_obj['humidity']
                tracker_device_obj.motion_sensor=tracker_decrypted_obj['motion_sensor']
                tracker_device_obj.position=tracker_decrypted_obj['position']
                tracker_device_obj.roll_angle=tracker_decrypted_obj['roll_angle']
                tracker_device_obj.pitch_angle=tracker_decrypted_obj['pitch_angle']
                tracker_device_obj.mac_time=tracker_decrypted_obj['mac_time']
                tracker_device_obj.temperature_sign=tracker_decrypted_obj['temperature_sign']
                tracker_device_obj.device=device
                tracker_device_obj.data=data
                tracker_device_obj.seqNumber = seqNumber
                # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
                # tracker_device_obj.timeStamp = time_data[0]
                # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
                # print('time_data',time_data)
                # tracker_device_obj.timeStamp = time_data
                tracker_device_obj.timeStamp=timeStamp
                tracker_device_obj.trip_id=trip_id
                tracker_device_obj.save()
            else:
                tracker_decrypted_obj=tracker_dcryted_payload_04_duplicate(data[5:])
                tracker_device_obj=TrackerDeviceIntergrations()
                tracker_device_obj.type=tracker_decrypted_obj['type']
                tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
                tracker_device_obj.battery_level=tracker_decrypted_obj['battery_level']
                tracker_device_obj.temperature=tracker_decrypted_obj['temperature']
                tracker_device_obj.humidity=tracker_decrypted_obj['humidity']
                tracker_device_obj.motion_sensor=tracker_decrypted_obj['motion_sensor']
                tracker_device_obj.position=tracker_decrypted_obj['position']
                tracker_device_obj.roll_angle=tracker_decrypted_obj['roll_angle']
                tracker_device_obj.pitch_angle=tracker_decrypted_obj['pitch_angle']
                tracker_device_obj.mac_time=tracker_decrypted_obj['mac_time']
                tracker_device_obj.temperature_sign=tracker_decrypted_obj['temperature_sign']
                tracker_device_obj.device=device
                tracker_device_obj.data=data
                tracker_device_obj.seqNumber = seqNumber
                # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
                # tracker_device_obj.timeStamp = time_data[0]
                # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
                # print('time_data',time_data)
                # tracker_device_obj.timeStamp = time_data
                tracker_device_obj.timeStamp=timeStamp
                tracker_device_obj.trip_id=trip_id
                tracker_device_obj.save()
        #=====need to update==========
        elif data[:2]=='05':
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_device_obj.type="Indoor new Mac ID"
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data'
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
        #=====need to update==========
        elif data[:2]=='06':
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_device_obj.type="Indoor Mac ID"
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data'
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
        #=====need to update==========  
        elif data[:2]=='07':
            tracker_decrypted_obj=tracker_dcryted_payload_07(data)
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_device_obj.type=tracker_decrypted_obj['type']
            tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
            tracker_device_obj.lat_degree=tracker_decrypted_obj['lat_degree']
            tracker_device_obj.lat_min1=tracker_decrypted_obj['lat_min1']
            tracker_device_obj.lat_min2=tracker_decrypted_obj['lat_min2']
            tracker_device_obj.lat_min3=tracker_decrypted_obj['lat_min3']
            tracker_device_obj.lon_degree=tracker_decrypted_obj['lon_degree']
            tracker_device_obj.lon_min2=tracker_decrypted_obj['lon_min2']
            tracker_device_obj.latitude=tracker_decrypted_obj['latitude']
            tracker_device_obj.longitude=tracker_decrypted_obj['longitude']
            tracker_device_obj.mac_time=tracker_decrypted_obj['mac_time']
            tracker_device_obj.address=tracker_decrypted_obj['address']
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
            
        elif data[:2]=='09' or data[:1]=='9' or data[:2]=='90' or  data[:2]=='91':
            tracker_decrypted_obj=tracker_dcryted_payload_09(data)
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_device_obj.type=tracker_decrypted_obj['type']
            tracker_device_obj.downlink_type=tracker_decrypted_obj['downlink_type']
            tracker_device_obj.alerttype=tracker_decrypted_obj['alerttype']
            tracker_device_obj.battery_level=tracker_decrypted_obj['battery_level']
            tracker_device_obj.low_battery_level=tracker_decrypted_obj['low_battery_level']
            tracker_device_obj.alert_temperature=tracker_decrypted_obj['alert_temperature']
            tracker_device_obj.alert_humidity=tracker_decrypted_obj['alert_humidity']
            tracker_device_obj.motion_sensor=tracker_decrypted_obj['motion_sensor']
            tracker_device_obj.tilt=tracker_decrypted_obj['tilt']
            tracker_device_obj.fall_detection=tracker_decrypted_obj['fall_detection']
            tracker_device_obj.theft=tracker_decrypted_obj['theft']
            tracker_device_obj.mac_time=tracker_decrypted_obj['mac_time']
            tracker_device_obj.position=tracker_decrypted_obj['old_position']
            tracker_device_obj.old_position=tracker_decrypted_obj['old_position']
            tracker_device_obj.new_position=tracker_decrypted_obj['new_position']
            tracker_device_obj.temperature_sign=tracker_decrypted_obj['temperature_sign']
            tracker_device_obj.temperature=tracker_decrypted_obj['temperature']
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
        elif data[:2]=='CE' or data[:2]=='0E':
            tracker_device_obj=TrackerDeviceIntergrations()
            tracker_device_obj.type="MAC Address"
            tracker_device_obj.device=device
            tracker_device_obj.data=data
            tracker_device_obj.seqNumber = seqNumber
            # time_data=[timeStamp if tracker_decrypted_obj['mac_time']=="RealTime" else (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S.%f %z")- timedelta(seconds=tracker_decrypted_obj['mac_time'])).strftime("%Y-%m-%d %H:%M:%S.%f %z")]
            # tracker_device_obj.timeStamp = time_data[0]
            # time_data=timeStamp_value_converted(tracker_decrypted_obj['mac_time'])
            # print('time_data',time_data)
            # tracker_device_obj.timeStamp = time_data
            tracker_device_obj.timeStamp=timeStamp
            tracker_device_obj.trip_id=trip_id
            tracker_device_obj.save()
        
        else:
            pass 
            # tracker_device_obj=TrackerDeviceIntergrations()
            # tracker_device_obj.device=device
            # tracker_device_obj.data=data
            # tracker_device_obj.save()
                
        trackerserializer=TrackerDeviceIntergrationAllDetailSerializer(tracker_device_obj)
        pay_load=trackerserializer.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "data upload successfully",
            'result': pay_load,
            'additional_data': {},
            }
        return Response(response_payload)
        
    
    
class TrackerDeviceInformation(viewsets.ViewSet):
    def list(self,request):
        queryset = TrackerDeviceIntergrations.objects.all().distinct('device')
        serializer_data = TrackerDeviceInfoSerializer(queryset,many=True)
        pay_load=serializer_data.data
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "",
            'result': pay_load,
            'additional_data': {},
        }
        return Response(response_payload)
    

class TrackerDeviceDetails(generics.GenericAPIView,PageNumberPagination):
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAllSerializer
    # pagination_class = PagePagination
   
    def get(self, request, slug=None):
        try:
            queryset = TrackerDeviceIntergrations.objects.filter(device=slug).order_by('-id')[0]
        except:
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': 'Device ID does not exist',
               "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        
        serializer = TrackerDeviceIntergrationAllSerializer(queryset)
        pay_load=serializer.data
        response_payload = {
        'is_authenticated': True,
        'status': status.HTTP_200_OK,
        'messages': "",
        'result': pay_load,
        'additional_data': {},
        }
        return Response(response_payload)
    
    
class DriverLanguageView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes=[UserRenderer]
    def get(self,request):
        qs=DriverLanguage.objects.filter(status=True)
        serializer_data=DriverLanguageSerialiser(qs,many=True)
        pay_load=serializer_data.data
        response_payload = {
        'is_authenticated': True,
        'status': status.HTTP_200_OK,
        'messages': "Language List fetch Successfully",
        'result': pay_load,
        'additional_data': {},
        }
        return Response(response_payload)
    
    def post(self,request):
        name=request.data.get('name')
        try:
            user = User.objects.get(id=str(request.user))
            # user = User.objects.get(id=id,role='driver')
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Driver id not valid please provided valid id',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        try:
            qs=DriverLanguage.objects.get(name=name)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Please enter the valid language',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        user.language_type=name
        user.save()
        # serializer = UserSerializer(user)
        # pay_load=serializer.data
        response_payload = {
        'is_authenticated': True,
        'status': status.HTTP_200_OK,
        'messages':'Language update successfully',
        "result": {},
        # 'result': pay_load,
        'additional_data': {},
        }
        return Response(response_payload)
    


class DriverTripRequestView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def list(self,request):
        # import pdb; pdb.set_trace()
        id=request.user.id
        print(id)
        trip_status=request.GET.get('trip_status')
        try:
            truck=Truck.objects.filter(driver_id=id).last()
            truck_id=truck.id
            print(truck_id)
        except :
            truck_id=None
        print(truck_id)
        if trip_status=='ongoing':
            queryset = Trip.objects.filter(truck_id=truck_id,trip_status='ongoing',payment_status='paid')
            # print(queryset)
            pay_load=[]
            if len(queryset)==0:
                response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages':"No record found.",
                'result':pay_load,
                'additional_data': {}
            }
                return Response(response_payload)
            else:
                for x in queryset:
                    print(x.truck.driver.id)
                    pay_load.append({
                        'destination':x.destination,
                        'starting_point':x.starting_point,
                        'trip_status':x.trip_status,
                        'helpline_number':x.helpiline_no,
                        'truck_id':x.truck_id,
                        'trip_id':x.id,
                        'trip_start_date':post_meridiem_time(x.driver_trip_start_date),
                        'trip_complete_date':x.driver_trip_complete_date,
                        "trip_id_show":x.trip_id_show,
                        "created_at":post_meridiem_date(x.created_at)
                    })
                response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages':"data fetched successfully",
                    'result':pay_load,
                    'additional_data': {}
                }
                return Response(response_payload)
        elif trip_status=='upcoming':
            print("ok")
            queryset = Trip.objects.filter(truck_id=truck_id,trip_status='upcoming',payment_status='paid').order_by('-starting_date', '-starting_time')
            print(queryset)
            pay_load=[]
            if len(queryset)==0:
                response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages':"No record found.",
                'result':pay_load,
                'additional_data': {}
            }
                return Response(response_payload)
                
            else:               
                for x in queryset:
                    pay_load.append({
                        'starting_date':x.starting_date,
                        'starting_time':x.starting_time,
                        'destination':x.destination,
                        'starting_point':x.starting_point,
                        'truck_type':x.truck_type,
                        'material_type':x.material.material_type,
                        'material_weight':x.submaterial.material_weight,
                        'submaterial':x.submaterial.material_subtype,
                        'created_at':x.created_at,
                        'trip_status':x.trip_status,
                        'amount':x.amount,
                        'trip_id':x.id,
                        'truck_id':x.truck_id,
                        'trip_start_date':x.driver_trip_start_date,
                        'trip_complete_date':x.driver_trip_complete_date,
                        "trip_id_show":x.trip_id_show,
                        "created_at":post_meridiem_date(x.created_at),
                        'constraints':{"temprature":x.submaterial.temprature,"humidity":x.submaterial.humidity,"tilt":x.submaterial.tilt,"ambient_light":x.submaterial.ambient_light,"pitch_angle":x.submaterial.pitch_angle,"roll_angle":x.submaterial.roll_angle}
                    })
                response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_201_CREATED,
                    'messages':"data fetched succesfully",
                    'result':pay_load,
                    'additional_data': {}
                }
                return Response(response_payload)
        elif trip_status=='completed':
            queryset=Trip.objects.filter(truck_id=truck_id,trip_status='completed',payment_status='paid').order_by('-driver_trip_complete_date')
            pay_load=[]
            if len(queryset)==0:
                response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages':"No record found.",
                'result':pay_load,
                'additional_data': {}
            }
                return Response(response_payload)
            else:
                for x in queryset:
                    pay_load.append({
                        'destination':x.destination,
                        'starting_point':x.starting_point,
                        'truck_type':x.truck_type,
                        'starting_time':x.starting_time,
                        'material_type':x.material.material_type,
                        'material_weight':x.submaterial.material_weight,
                        'submaterial':x.submaterial.material_subtype,
                        'created_at':x.created_at,
                        'trip_status':x.trip_status,
                        'amount':x.amount,
                        'truck_id':x.truck_id,
                        'trip_id':x.id,
                        'trip_start_date':post_meridiem_time(x.driver_trip_start_date),
                        'trip_complete_date':post_meridiem_time(x.driver_trip_complete_date),
                        'feedback':x.feedback,
                        'issue':x.issue,
                        'rating':x.rating,
                        "trip_id_show":x.trip_id_show,
                        "created_at":post_meridiem_date(x.created_at)
                    })
                response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages':"data fetched succesfully",
                    'result':pay_load,
                    'additional_data': {}
                }
                return Response(response_payload)
            
        else:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Invalid URL",
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        

class DriverTripStartOTPView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        id=request.user.id
        # id = request.data.get('id')
        # print(id)
        trip_id=request.data.get('trip_id')
        mobile = request.data.get('mobile')
        country_code = request.data.get('country_code')
        id=request.user.id
        print(id)
        if not trip_id or not mobile or not country_code:
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Trip ID not found.',
                        "result": {},
                        'additional_data': {},
                        
                    }
            return Response(response_payload)
        try:
            user = User.objects.get(id=id, mobile=mobile)
            print(user.mobile)
            # mobile=user.mobile
            # country_code=user.country_code
            print(country_code)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'This number is not associated with this driver.',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload) 
        
        otp=send_otp(mobile,country_code)["otp"]
        print(otp)
        try:
            Trip.objects.filter(id=trip_id).exists()
            result=Trip.objects.filter(id=trip_id).update(driver_start_otp=otp)
            result=Trip.objects.filter(id=trip_id).update(driver_otp_time=int(float((datetime.now().timestamp()))))
            response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    'messages': "OTP send successfully.",
                    "result": {},
                    'additional_data': {},
                }
            return Response(response_payload)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Trip id not valid',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload) 



class DriverVerifyOTPView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def create(self, request):
        id=request.user.id
        # id = request.data.get('id')
        print("######",id)
        otp = request.data.get('otp')
        mobile = request.data.get('mobile')
        trip_id=request.data.get('trip_id')
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number not provided',
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not otp:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'otp not provided',
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        try:
            user = User.objects.get(mobile=mobile, role='driver')
            print(user)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Mobile number not valid',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload) 
        res=Trip.objects.filter(id=trip_id)
        print("res", res)
        trip_obj = Trip.objects.filter(id=trip_id)
        print(trip_obj)
        try:
            trip_obj = Trip.objects.get(id=trip_id)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Trip not found for the driver',
               "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        if  trip_obj.driver_start_otp==otp:
            current_time=datetime.now().timestamp()
            print(current_time)
            if int(float(current_time))-int(trip_obj.driver_otp_time)<3000:
                trip_obj.trip_status="ongoing"
                trip_obj.driver_trip_start_date=datetime.now()
                trip_obj.save()
                try:
                    try:
                        user = User.objects.filter(fcm_token__isnull=False, id=str(trip_obj.admin)).values('fcm_token')
                        fcm_tokens_admin = [item['fcm_token'] for item in user] 
                        print(fcm_tokens_admin)
                        firebase_object=FirePushNotication.objects.filter(fire_type='Trip start notification', role='admin').last()
                        # send_notification(fcm_tokens, firebase_object.title , firebase_object.description)
                        send_notification(fcm_tokens_admin, "Trip Started" , "Your Trip has been started")
                        print("Notification sent to Admin")
                        print(trip_obj.user)
                        print(type(trip_obj.user))
                        user = User.objects.filter(fcm_token__isnull=False, id=str(trip_obj.user)).values('fcm_token')
                        fcm_tokens_customer = [item['fcm_token'] for item in user]
                        print(fcm_tokens_customer)
                        firebase_object=FirePushNotication.objects.filter(fire_type='Trip start notification', role='customer').last()
                        # send_notification(fcm_tokens1, firebase_object.title , firebase_object.description)
                        send_notification(fcm_tokens_customer, "Trip Started" , "Your Trip has been started")
                        print("Notification sent to Customer")

                        driver = User.objects.filter(id=id, fcm_token__isnull=False).values("fcm_token")
                        fcm_token_driver = [item['fcm_token'] for item in driver]
                        send_notification(fcm_token_driver, "Trip Started" , "Your Trip has been started")
                        print("Notification sent to Driver")
                    except:
                        pass

                    #return Response({"messages":"notification sent"})
                    response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    "messages":"OTP verified. Your Trip has been marked as started.",
                    "notification_status":"Successful",
                    "result": {},
                    'additional_data': {},
                }

                    return Response(response_payload)
                except:
                    response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    "messages":"OTP verified but some issue occurred while notifying to Vendor and Customer.",
                    "notification_status":"Failed",
                    "result": {},
                    'additional_data': {},
                }

                return Response(response_payload)
            else:
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Your otp number has been expire. Please login again.',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        else:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Please enter valid OTP',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)

    



class CompleteTripOTPsendView(viewsets.ViewSet):
    # permission_classes=(IsAuthenticated)
    def create(self, request):
        id=request.user.id
        print("######",id)
        trip_id=request.data.get('trip_id')
        if not trip_id:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Trip ID not provided',
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        try:
            trip_obj = Trip.objects.get(id=trip_id)
            mobile=trip_obj.admin.mobile
            print(mobile)
            country_code=trip_obj.admin.country_code
            print(country_code)
            # trip_obj.trip_status="completed"
            # trip_obj.driver_trip_complete_date=datetime.now()
            

            otp=send_otp(mobile,country_code)["otp"]
            print(otp)
            try:
                result=Trip.objects.filter(id=trip_id).update(driver_complete_otp=otp)
                result=Trip.objects.filter(id=trip_id).update(driver_complete_otp_time=int(float((datetime.now().timestamp()))))
                response_payload = {
                        'is_authenticated': True,
                        'status':status.HTTP_200_OK,
                        'messages': "OTP send successfully to your Vendor.",
                        "result": {},
                        'additional_data': {},
                    }
                return Response(response_payload)
            except:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages':'Trip id not valid',
                    "result": {},
                    'additional_data': {},
                }

                return Response(response_payload) 

        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Trip not found for the driver',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
    
           


class DriverfetchremarkView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def list(self,request):
        id=request.user.id
        queryset = Trip.objects.filter(truck__driver_id=id,trip_status='completed',feedback__isnull=False)
        if len(queryset) !=0:
            trip_serializer=FeebbackTripSerializer(queryset,many=True)
            data=trip_serializer.data
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages':"data fetched successfully",
                'result':data,
                'additional_data': {}
            }
            return Response(response_payload)
        else:
            response_payload = {    
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages':"No Feed back available",
                'result':{},
                'additional_data': {}
            }
            return Response(response_payload)



class TripCompleteVerifyOTPView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def create(self, request):
        # import pdb; pdb.set_trace()
        id=request.user.id
        print("######",id)
        otp = request.data.get('otp')
        #mobile = request.data.get('mobile')
        trip_id=request.data.get('trip_id')
        if not otp:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'otp not provided',
                "result": {},
                'additional_data': {},
            }
            return Response(response_payload)
        try:
            trip_obj = Trip.objects.get(id=trip_id)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Trip not found for the driver',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        if  trip_obj.driver_complete_otp==otp:
            current_time=datetime.now().timestamp()
            # print(current_time)
            if int(float(current_time))-int(trip_obj.driver_complete_otp_time)<18000:
                trip_obj.trip_status="completed"
                trip_obj.driver_trip_complete_date=datetime.now()
                trip_obj.save()
                try:
                    truck_id=trip_obj.truck.id
                    # print(truck_id)
                    if truck_id:
                        Truck.objects.filter(id=truck_id).update(avail_status='True')
                        # print("well done")
                    else:
                        pass
                except:
                    pass
                try:
                    user = User.objects.filter(fcm_token__isnull=False, id=str(trip_obj.admin)).values('fcm_token')
                    fcm_tokens = [item['fcm_token'] for item in user] 
                    print(fcm_tokens)
                    firebase_object=FirePushNotication.objects.filter(fire_type='Trip end notification', role='admin').last()
                    send_notification(fcm_tokens, firebase_object.title , firebase_object.description)
                    print("Notification sent to Admin")
                    print(trip_obj.user)
                    print(type(trip_obj.user))
                    user = User.objects.filter(fcm_token__isnull=False, id=str(trip_obj.user)).values('fcm_token')
                    fcm_tokens1 = [item['fcm_token'] for item in user] 
                    print(fcm_tokens1)
                    firebase_object=FirePushNotication.objects.filter(fire_type='Trip end notification', role='customer').last()
                    send_notification(fcm_tokens1, firebase_object.title , firebase_object.description)
                    print("Notification sent to Customer")
                    #return Response({"messages":"notification sent"})

                    response_payload = {
                        'is_authenticated': True,
                        'status':status.HTTP_200_OK,
                        "messages":"OTP verified. Your Trip has been marked as completed",
                        "notification_status":"Successful",
                        "result": {},
                        'additional_data': {},
                    }

                    return Response(response_payload)
                except:
                    response_payload = {
                        'is_authenticated': True,
                        'status':status.HTTP_200_OK,
                        "messages":"Your trip has been marked as completed. But some issue occured while notifying to your Vendor and Customer.",
                        "notification_status":"Failed",
                        "result": {},
                        'additional_data': {},
                    }

                    return Response(response_payload)
            else:
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'your otp number has been Expire.',
                 "result": {},
                'additional_data': {},
            }

            return Response(response_payload)
        else:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Please enter valid OTP',
                "result": {},
                'additional_data': {},
            }

            return Response(response_payload)