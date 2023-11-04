from django.http import JsonResponse
from django.shortcuts import render
import googlemaps
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from customer.api.views import send_notification
from customer.models import FirePushNotication, MobileOTP, User
from adminapp.models import AdminProfile, AdminResponse, AdminTripDetails, Trip,Truck
from adminapp.api.serializers import AdminSerializer,FleetViewSerializer, PaymentStatusSerializer,VechicleTruckSerializer,DriverGetSerializer,AdminAddDeriverSerializer,\
    TripOngoingSerializer,TrackerDeviceIntergrationsAdminLocationSerializer,TrackerDeviceIntergrationsAdminDetailSerializer,AllTripOngoingSerializer,AllTrackerDeviceIntergrationsAdminLocationSerializer
import re
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework_simplejwt.serializers import RefreshToken
from django.contrib.auth import authenticate
from customer.api.sendmobileotp import custom_send_otp,send_otp
from driverapp.api.serializers import TrackerDeviceIntergrationSerializer
from datetime import datetime
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from driverapp.models import TrackerDeviceIntergrations
from driverapp.api.serializers import TrackerDeviceIntergrationAlertSerializer
from adminapp.models import AddDriver,AdminAccounts
from django.core.serializers import serialize
from rest_framework.pagination import PageNumberPagination
from geopy.geocoders import Nominatim
from driverapp.api.serializers import TrackerDeviceIntergrationAllSerializer
from superadmin.models import HelpDeskQuery, TrackerDeviceInfo
from utils.views import post_meridiem_time

class AdminappView(viewsets.ViewSet):
    def list(self, request):
        return Response({"message":"admin app"})


class AdminRegisterView(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    def create(self, request):
        company_name = request.data.get('company_name')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        mobile = request.data.get('mobile')
        country_code = request.data.get('country_code')
        email = request.data.get('email')
        gst = request.data.get('gst')
        pan_number = request.data.get('pan_number')
        address=request.data.get('address')
        password = request.data.get('password')
        confirmPassword = request.data.get('confirm_password') or request.data.get('confirmPassword')
        role=request.data.get('role')
        fcm_token=request.data.get('fcm_token')
        print("fcm token",fcm_token)
        if not company_name:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Company name is not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if AdminProfile.objects.filter(company_name=company_name).exists():
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "This company name is already registered with us",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not first_name:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "First name not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not last_name:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Last name not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Mobile number not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if User.objects.filter(mobile=mobile).exists():
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "User with this mobile number already exists",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not country_code:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Country Code not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not email:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Email ID not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if User.objects.filter(email=email).exists():
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "User with this email already exists",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
            
        if not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email):
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Email ID not valid",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
            
        if not gst:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "gst not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not pan_number:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "pan number not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not len(pan_number)<=10:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Pan number not is not greater than 10 digit",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not address:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':  "address not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        
        if not password:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':  "Password not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        if not confirmPassword:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':  "confirm Password  not provided",
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)

        if password != confirmPassword:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':  ' Password did not match ',
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        user_object = User()
        user_object.first_name=first_name
        user_object.last_name=last_name
        user_object.email = email.lower()
        user_object.set_password(password)
        user_object.mobile = mobile
        user_object.country_code = country_code
        user_object.role="admin"
        user_object.is_active=False
        user_object.fcm_token=fcm_token
        user_object.save()
            
        profile, created=AdminProfile.objects.get_or_create(user=user_object, gst=gst,pan_number=pan_number,company_name=company_name)
        profile.save()
        response_payload = {
            'is_authenticated': True,
            'status':status.HTTP_200_OK,
            'messages': 'Registration successfull',
            'result': {},
            'additional_data': {},
        }
        return Response(response_payload)
    
class SendOtpView(viewsets.ViewSet):
    def create(self,request):
        mobile = request.data.get('mobile')
        country_code = request.data.get('country_code')
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number not provided',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not country_code:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'country code not provided',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        
        try:
            user_object = User.objects.get(mobile=mobile,country_code=country_code,role='admin')
        except:
            
            response_payload = {
            'is_authenticated': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'messages': 'Mobile number or country code not valid',
            'result': [],
            'additional_data': {},
            }
            return Response(response_payload)
        if user_object:
            otp_object,created =MobileOTP.objects.get_or_create(user=user_object)
            otp_object.mobile=mobile
            otp_object.otp=send_otp(mobile,country_code)["otp"]
            otp_object.time=int(float((datetime.now().timestamp())))
            otp_object.save()
            response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_201_CREATED,
            "mobile_no":str(user_object.mobile),
            'messages': 'OTP send succesfully on your mobile number',
            'result': [],
            'additional_data': {},
            }
            return Response(response_payload)
        
class VerifyOtpView(viewsets.ViewSet):
    def create(self,request):
        otp = request.data.get('otp')
        mobile = request.data.get('mobile')
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number not provided',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not otp:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'otp not provided',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        try:
            mobile_otp = MobileOTP.objects.get(user__mobile=mobile)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Mobile number not valid',
                'result': [],
                'additional_data': {},
            }

            return Response(response_payload)
        if  mobile_otp.otp==otp:
            current_time=datetime.now().timestamp()
            if int(float(current_time))-int(mobile_otp.time)<300:
                mobile_otp.otp_verify = True
                mobile_otp.count +=1
                mobile_otp.save()
                response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    "messages":"Successful",
                    'result': [],
                    'additional_data': {},
                }
                return Response(response_payload)
            else:
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'your otp number has been Expire  please login again',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        else:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Please enter valid OTP',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
class ResetPasswordView(viewsets.ViewSet):
    def create(self,request):
        mobile=request.data.get('mobile')
        new_password=request.data.get('new_password')
        confirm_password=request.data.get('confirm_password')
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please provide mobile number',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not new_password:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your new password',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if User.objects.filter(mobile=mobile,role='admin'):
            if new_password==confirm_password:
                user=User.objects.get(mobile=mobile)
                user.set_password(new_password)
                user.save()
                response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': 'password updated succesfully',
                'result': [],
                'additional_data': {},
            }
                return Response(response_payload)
            else:
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'both passwords dont match',
                'result': [],
                'additional_data': {},
            }
                return Response(response_payload)
        else:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number not registered',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)


class LoginViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = AdminSerializer
    permission_classes = (AllowAny,)
    def create(self, request):
        try:
            password = request.data.get('password')
            email = request.data.get('email')
            fcm_token=request.data.get('fcm_token')
            print("fcm token",fcm_token)
            if not email:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "email / passowrd is not provided",
                    'result': {},
                    'additional_data': {},
                }
                return Response(response_payload)
                # error_object['email']="email is not provided"
                # error_flag=True
                
            if email:
                mail_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                if not (re.search(mail_regex, email)):
                    response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages':  "Invalid email id",
                    'result': {},
                    'additional_data': {},
                    }
                    return Response(response_payload)
            if not password:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Password is not provided.",
                    'result': {},
                    'additional_data': {},
                }
                return Response(response_payload)
                    
            try:
                user=User.objects.get(email=email,role='admin',is_active=True)
                user.fcm_token=fcm_token
                user.save()
            except Exception as e:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': 'User does not exist.',
                    'result': {},
                    'additional_data': {},
                }

                return Response(response_payload)
            if user.email !=email:
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Please enter valid Email',
                'result': {},
                'additional_data': {},
                }
                return Response(response_payload)
            if not user.check_password(password):
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Please enter valid Passoword',
                'result': {},
                'additional_data': {},
                }
                return Response(response_payload)
            
            refresh_token=RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            refresh_token = str(refresh_token)     
            profile,created=AdminProfile.objects.get_or_create(user=user)
            login_serializer=AdminSerializer(profile)
            login_data=login_serializer.data
            
            response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                "messages":"Login Successful",
                'result': login_data,
                'access_token': access_token,
                'refresh_token': refresh_token,    
                'additional_data': {},
            }
            return Response(response_payload)
        except Exception as e:
            response_payload = {
                        'is_authenticated': True,
                        'status':500,
                        "messages":f'login error message{str(e)}',
                        "result":{},
                        'additional_data': {},
                    }
            return Response(response_payload)
        


class ALLDeviceAlertView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAlertSerializer
    def get(self, request):
        try:
            queryset = TrackerDeviceIntergrations.objects.filter(type='Alert Data').order_by('-id')
        except Exception as e:
            response_payload = {
            'is_authenticated': False,
            'status':status.HTTP_400_BAD_REQUEST,
            'messages': "Invalid tracker id",
            'result': [],
            'additional_data': {},
            }
            return Response(response_payload)     
        if queryset is not None:
            serializer = TrackerDeviceIntergrationAlertSerializer(queryset,many=True)
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
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
       
from driverapp.api.base64 import base64_file
 
class FleetAddView(viewsets.ViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes=(IsAuthenticated,)
    def create(self,request):
        admin_id=request.user.id
        chassis_no=request.data.get('chassis_no')
        rc=request.FILES.get('rc')
        type=request.data.get('type')
        capacity=request.data.get('capacity')
        width=request.data.get('width')
        height=request.data.get('height')
        tyre_count=request.data.get('tyre_count')
        truck_no=request.data.get('truck_no')
        manufacturer=request.data.get('manufacturer')
        container_no=request.data.get('container_no')
        registration_date=request.data.get('registration_date')
        rc_expiry=request.data.get('rc_expiry')
        pollution_certificate=request.data.get('pollution_certificate')
        rc1=request.data.get('rc1')
        pollution_certificate1=request.data.get('pollution_certificate1')
        pollution_expiry=request.data.get('pollution_expiry')
        
        if len(chassis_no) !=17:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter valid chassis number",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not re.match("^[0-9]{1,9}",capacity):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid capacity",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not re.match("^[0-9]{1,4}$",height):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid height",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not re.match("^[0-9]{1,4}$",tyre_count):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid tyre count",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if Truck.objects.filter(truck_no=truck_no,chassis_no=chassis_no,is_deleted='False').exists():
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "this truck already exists",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",registration_date):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid registration date",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)

        if not rc_expiry:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid rc expiry date",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",rc_expiry):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid rc expiry date",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",pollution_expiry):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid pollution expiry date",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not re.match("^[0-9]{1,3}$",width):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid width",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not (chassis_no  and type and capacity and height and tyre_count and truck_no and tyre_count and container_no and registration_date and width and pollution_expiry and rc_expiry  and manufacturer):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Please specify all the details",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if User.objects.filter(id=admin_id,role='admin').exists():
            if rc1 is not None:
                truck_obj=Truck()
                truck_obj.admin_id=admin_id
                truck_obj.chassis_no=chassis_no
                truck_obj.rc= base64_file(rc1)
                truck_obj.type=type
                truck_obj.capacity=capacity
                truck_obj.width=width
                truck_obj.height=height
                truck_obj.tyre_count=tyre_count
                truck_obj.truck_no=truck_no
                truck_obj.manufacturer=manufacturer
                truck_obj.container_no=container_no
                truck_obj.registration_date=registration_date
                truck_obj.rc_expiry=rc_expiry
                truck_obj.pollution_certificate=base64_file(pollution_certificate1)
                truck_obj.pollution_expiry=pollution_expiry
                truck_obj.avail_status=True 
                truck_obj.save()
                response_payload = {
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages': "fleet added successfully",
                    'result': [],
                    'additional_data': {},
                }
                return Response(response_payload)
            
            else:
                truck_obj=Truck()
                truck_obj.admin_id=admin_id
                truck_obj.chassis_no=chassis_no
                truck_obj.rc=rc
                truck_obj.type=type
                truck_obj.capacity=capacity
                truck_obj.width=width
                truck_obj.height=height
                truck_obj.tyre_count=tyre_count
                truck_obj.truck_no=truck_no
                truck_obj.manufacturer=manufacturer
                truck_obj.container_no=container_no
                truck_obj.registration_date=registration_date
                truck_obj.rc_expiry=rc_expiry
                truck_obj.pollution_certificate=pollution_certificate
                truck_obj.pollution_expiry=pollution_expiry
                truck_obj.avail_status=True 
                truck_obj.save()
                response_payload = {
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages': "fleet added successfully",
                    'result': [],
                    'additional_data': {},
                }
                return Response(response_payload)
            # else:
            #     pass
                # response_payload = {
                #     'is_authenticated': False,
                #     'status':status.HTTP_400_BAD_REQUEST,
                #     'messages': "please enter   valid details",
                #     'result': [],
                #     'additional_data': {},
                #     }
                # return Response(response_payload)
                
            # Truck.objects.create(admin_id=admin_id,chassis_no=chassis_no,rc=base64_file(rc),type=type,capacity=capacity,height=height,tyre_count=tyre_count,truck_no=truck_no,manufacturer=manufacturer,
            #                      container_no=container_no,registration_date=registration_date,rc_expiry=rc_expiry,pollution_certificate=base64_file(pollution_certificate),
            #                      pollution_expiry=pollution_expiry,width=width,avail_status='True')
            # truck=Truck.objects.filter(user_id=admin_id).values('id')
            
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "admin id does not exists",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
    def list(self,request):
        admin_id=request.user.id
        if not admin_id:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Please provide admin id",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        admin_obj=Truck.objects.filter(admin_id=admin_id,is_verified=True,is_deleted=False)
        serializer=FleetViewSerializer(admin_obj,many=True)
        if Truck.objects.filter(admin_id=admin_id).exists():
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': "data fetched succesfully",
                'result': serializer.data,
                'additional_data': {},
            }
            return Response(response_payload)
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "admin id not found",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
    def update(self,request):
        admin_id=request.user.id
        type=request.data.get('type')
        capacity=request.data.get('capacity')
        width=request.data.get('width')
        height=request.data.get('height')
        tyre_count=request.data.get('tyre_count')
        manufacturer=request.data.get('manufacturer')
        container_no=request.data.get('container_no')
        registration_date=request.data.get('registration_date')
        rc_expiry=request.data.get('rc_expiry')
        pollution_expiry=request.data.get('pollution_expiry')
        truck_id=request.data.get('truck_id')
        truck_no=request.data.get('truck_no')
        chassis_no=request.data.get('chassis_no')
        driver_id=request.data.get('driver_id')
        supervisor_id=request.data.get('supervisor_id')
        tracker_id=request.data.get('tracker_id')
        rc1=request.data.get('rc1')
        pollution_certificate1=request.data.get('pollution_certificate1')
        rc=request.data.get('rc')
        pollution_certificate=request.data.get('pollution_certificate')
        pollution_certificate1= [ None  if pollution_certificate1 is "" else pollution_certificate1][0]
        rc1= [ None  if rc1 is "" else rc1][0]
        print("pollution_certificateff",pollution_certificate1)
        print("rc1",rc1)
        if not (admin_id and truck_id):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Please provide admin and truck id",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if len(chassis_no) !=17:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter valid chassis number",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not capacity:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid capacity",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
    
        if not re.match("^[0-9]{1,4}$",height):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid height",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not re.match("^[0-9]{1,4}$",tyre_count):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid tyre count",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",pollution_expiry):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid pollution expiry date",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)

        if not re.match("^[0-9]{1,3}$",width):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid width",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",registration_date):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid registration date",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",rc_expiry):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid rc expiry date",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        if not (chassis_no and  type and capacity and height and tyre_count and truck_no and tyre_count and container_no and registration_date
                and width and pollution_expiry and rc_expiry  and manufacturer):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Please specify all the details",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if Truck.objects.filter(id=truck_id,admin_id=admin_id).exists():
            try:
                truck_obj=Truck.objects.get(id=truck_id)
                existing_driver=truck_obj.driver
                existing_tracker=truck_obj.tracker_id
                print(existing_tracker)
                # print(existing_driver.id)
            except:
                pass
            if driver_id:
                if existing_driver and existing_driver.id != driver_id:
                    try:
                        User.objects.filter(id=existing_driver.id).update(driver_status='Available')
                        AddDriver.objects.filter(driver_id=existing_driver.id).update(status=True)
                    except:
                        pass  # Handle the exception appropriately

                try:
                    User.objects.filter(id=driver_id).update(driver_status='On Trip')
                    AddDriver.objects.filter(driver_id=driver_id).update(status=False)
                except:
                    pass  # Handle the exception appropriately
            # existing_tracker = Truck.objects.get(id=truck_id,)
            try:
                if tracker_id:
                    if existing_tracker:
                        if existing_tracker == tracker_id:
                            TrackerDeviceInfo.objects.filter(admin_id=admin_id,device=tracker_id).update(tracker_assigned='True')
                        else:
                            TrackerDeviceInfo.objects.filter(admin_id=admin_id,device=existing_tracker).update(tracker_assigned='False')
                            TrackerDeviceInfo.objects.filter(admin_id=admin_id,device=tracker_id).update(tracker_assigned='True')
                    else:
                        TrackerDeviceInfo.objects.filter(admin_id=admin_id,device=tracker_id).update(tracker_assigned='True')
                else: 
                    None
            except:
                None
            Truck.objects.filter(id=truck_id,admin_id=admin_id).update(truck_no=truck_no,chassis_no=chassis_no,type=type,capacity=capacity,height=height,tyre_count=tyre_count,driver_id=driver_id,supervisor_id=supervisor_id,
                                                                      container_no=container_no,registration_date=registration_date,width=width,pollution_expiry=pollution_expiry,rc_expiry=rc_expiry,
                                                                       manufacturer=manufacturer,tracker_id=tracker_id)
            truck_obj=Truck.objects.get(id=truck_id)
            existing_driver=truck_obj.driver
            if rc1 is None and pollution_certificate1 is None:
                truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
            
            elif rc1 is not None:
                truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
                truck.rc=base64_file(rc1)
                truck.save()
            elif pollution_certificate1 is not None:
                truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
                truck.pollution_certificate=base64_file(pollution_certificate1)
                truck.save()
            elif rc is None and pollution_certificate is None:
                truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
            elif rc is not None:
                truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
                truck.rc=rc
                truck.save()
            elif pollution_certificate is not None:
                truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
                truck.pollution_certificate=pollution_certificate
                truck.save()
            else:
                pass
            admin_obj=Truck.objects.filter(id=truck_id,admin_id=admin_id)
            serializer=FleetViewSerializer(admin_obj,many=True)
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': "data updated succesfully",
                'result': serializer.data,
                'additional_data': {},
            }
            return Response(response_payload)
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "truck id not found",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
    def destroy(self,request):
        admin_id=request.user.id
        truck_id=request.GET.get('truck_id')
        if not (admin_id and truck_id):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Please provide admin and truck id",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if Truck.objects.filter(id=truck_id,admin_id=admin_id).exists():
            Truck.objects.filter(id=truck_id,admin_id=admin_id).update(is_deleted='True',avail_status='False',is_verified='False')
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': "data deleted succesfully",
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "id not found",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
# class FleetUpdateCrudAPIView(viewsets.ViewSet):
#     # parser_classes = [MultiPartParser, FormParser]
#     permission_classes=(IsAuthenticated,)
#     def list(self,request):
#         admin_id=request.user.id
#         if not admin_id:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "Please provide admin id",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         admin_obj=Truck.objects.filter(admin_id=admin_id,is_verified=True,is_deleted=False)
#         serializer=FleetViewSerializer(admin_obj,many=True)
#         if Truck.objects.filter(admin_id=admin_id).exists():
#             response_payload = {
#                 'is_authenticated': True,
#                 'status': status.HTTP_200_OK,
#                 'messages': "data fetched succesfully",
#                 'result': serializer.data,
#                 'additional_data': {},
#             }
#             return Response(response_payload)
#         else:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "admin id not found",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#     def create(self,request):
#         admin_id=request.user.id
#         chassis_no=request.data.get('chassis_no')
#         rc=request.FILES.get('rc')
#         rc1=request.data.get('rc1')
#         type=request.data.get('type')
#         capacity=request.data.get('capacity')
#         width=request.data.get('width')
#         height=request.data.get('height')
#         tyre_count=request.data.get('tyre_count')
#         truck_no=request.data.get('truck_no')
#         manufacturer=request.data.get('manufacturer')
#         container_no=request.data.get('container_no')
#         registration_date=request.data.get('registration_date')
#         rc_expiry=request.data.get('rc_expiry')
#         pollution_certificate=request.data.get('pollution_certificate')
#         pollution_certificate1=request.data.get('pollution_certificate1')
#         pollution_expiry=request.data.get('pollution_expiry')
        
#         if len(chassis_no) !=17:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter valid chassis number",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not re.match("^[0-9]{1,9}",capacity):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid capacity",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not re.match("^[0-9]{1,4}$",height):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid height",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not re.match("^[0-9]{1,4}$",tyre_count):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid tyre count",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if Truck.objects.filter(truck_no=truck_no,chassis_no=chassis_no,is_deleted='False').exists():
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "this truck already exists",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",registration_date):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid registration date",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)

#         if not rc_expiry:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid rc expiry date",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",rc_expiry):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid rc expiry date",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",pollution_expiry):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid pollution expiry date",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if not re.match("^[0-9]{1,3}$",width):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid width",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not (chassis_no  and type and capacity and height and tyre_count and truck_no and tyre_count and container_no and registration_date and width and pollution_expiry and rc_expiry  and manufacturer):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "Please specify all the details",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         # print('oimage',base64_file(rc))
#         # print('pollution_certificate',base64_file(pollution_certificate))
#         if User.objects.filter(id=admin_id,role='admin').exists():
#             print('rc',rc)
#             if rc1 is not None:
#                 truck_obj=Truck()
#                 truck_obj.admin_id=admin_id
#                 truck_obj.chassis_no=chassis_no
#                 # truck_obj.rc=rc
#                 truck_obj.rc1= base64_file(rc1)
#                 truck_obj.type=type
#                 truck_obj.capacity=capacity
#                 truck_obj.width=width
#                 truck_obj.height=height
#                 truck_obj.tyre_count=tyre_count
#                 truck_obj.truck_no=truck_no
#                 truck_obj.manufacturer=manufacturer
#                 truck_obj.container_no=container_no
#                 truck_obj.registration_date=registration_date
#                 truck_obj.rc_expiry=rc_expiry
#                 # truck_obj.pollution_certificate=pollution_certificate
#                 truck_obj.pollution_certificate1=base64_file(pollution_certificate1)
#                 truck_obj.pollution_expiry=pollution_expiry
#                 truck_obj.avail_status=True 
#                 truck_obj.save()
#                 response_payload = {
#                     'is_authenticated': True,
#                     'status': status.HTTP_200_OK,
#                     'messages': "fleet added successfully",
#                     'result': [],
#                     'additional_data': {},
#                 }
#                 return Response(response_payload)
            
#             else:
#                 # print('rc1',rc1)
#                 print('pollution_certificate1',pollution_certificate1)
#                 truck_obj=Truck()
#                 truck_obj.admin_id=admin_id
#                 truck_obj.chassis_no=chassis_no
#                 truck_obj.rc=rc
#                 # truck_obj.rc1= base64_file(rc1)
#                 truck_obj.type=type
#                 truck_obj.capacity=capacity
#                 truck_obj.width=width
#                 truck_obj.height=height
#                 truck_obj.tyre_count=tyre_count
#                 truck_obj.truck_no=truck_no
#                 truck_obj.manufacturer=manufacturer
#                 truck_obj.container_no=container_no
#                 truck_obj.registration_date=registration_date
#                 truck_obj.rc_expiry=rc_expiry
#                 truck_obj.pollution_certificate=pollution_certificate
#                 # truck_obj.pollution_certificate1=base64_file(pollution_certificate1)
#                 truck_obj.pollution_expiry=pollution_expiry
#                 truck_obj.avail_status=True 
#                 truck_obj.save()
#                 response_payload = {
#                     'is_authenticated': True,
#                     'status': status.HTTP_200_OK,
#                     'messages': "fleet added successfully",
#                     'result': [],
#                     'additional_data': {},
#                 }
#                 return Response(response_payload)
            
#         else:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "admin id does not exists",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
    
#     def update(self,request):
#         admin_id=request.user.id
        
#         type=request.data.get('type')
#         capacity=request.data.get('capacity')
#         width=request.data.get('width')
#         height=request.data.get('height')
#         tyre_count=request.data.get('tyre_count')
#         manufacturer=request.data.get('manufacturer')
#         container_no=request.data.get('container_no')
#         registration_date=request.data.get('registration_date')
#         rc_expiry=request.data.get('rc_expiry')
#         pollution_expiry=request.data.get('pollution_expiry')
#         truck_id=request.data.get('truck_id')
#         truck_no=request.data.get('truck_no')
#         chassis_no=request.data.get('chassis_no')
#         driver_id=request.data.get('driver_id')
#         supervisor_id=request.data.get('supervisor_id')
#         tracker_id=request.data.get('tracker_id')
#         rc1=request.data.get('rc1')
#         pollution_certificate1=request.data.get('pollution_certificate1')
#         rc=request.data.get('rc')
#         pollution_certificate=request.data.get('pollution_certificate')
#         if not (admin_id and truck_id):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "Please provide admin and truck id",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if len(chassis_no) !=17:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter valid chassis number",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if not re.match("^[0-9]{1,9}$",capacity):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid capacity",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
    
#         if not re.match("^[0-9]{1,4}$",height):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid height",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if not re.match("^[0-9]{1,4}$",tyre_count):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid tyre count",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",pollution_expiry):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid pollution expiry date",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)

#         if not re.match("^[0-9]{1,3}$",width):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid width",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",registration_date):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid registration date",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",rc_expiry):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "please enter a valid rc expiry date",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
        
#         if not (chassis_no and  type and capacity and height and tyre_count and truck_no and tyre_count and container_no and registration_date
#                 and width and pollution_expiry and rc_expiry  and manufacturer):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "Please specify all the details",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if Truck.objects.filter(id=truck_id,admin_id=admin_id).exists():
#             Truck.objects.filter(id=truck_id,admin_id=admin_id).update(truck_no=truck_no,chassis_no=chassis_no,type=type,capacity=capacity,height=height,tyre_count=tyre_count,driver_id=driver_id,supervisor_id=supervisor_id,
#                                                                       container_no=container_no,registration_date=registration_date,width=width,pollution_expiry=pollution_expiry,rc_expiry=rc_expiry,
#                                                                        manufacturer=manufacturer,tracker_id=tracker_id)
#             try:
#                 User.objects.filter(id=driver_id).update(driver_status='On Trip')
#                 AddDriver.objects.filter(driver_id=driver_id).update(status='False')
#             except:
#                 None
#             try:
#                 if tracker_id:
#                     TrackerDeviceInfo.objects.filter(admin_id=admin_id,device=tracker_id).update(tracker_assigned='True')
#                 else: 
#                     None
#             except:
#                 None
#             if rc1 is None and pollution_certificate1 is None:
#                 truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
            
#             elif rc1 is not None:
#                 truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
#                 truck.rc=base64_file(rc1)
#                 truck.save()
#             elif pollution_certificate1 is not None:
#                 truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
#                 truck.pollution_certificate=base64_file(pollution_certificate1)
#                 truck.save()
#             elif rc is None and pollution_certificate is None:
#                 truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
#             elif rc is not None:
#                 truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
#                 truck.rc=rc
#                 truck.save()
#             elif pollution_certificate is not None:
#                 truck=Truck.objects.get(id=truck_id,admin_id=admin_id)
#                 truck.pollution_certificate=pollution_certificate
#                 truck.save()
#             else:
#                 pass
#             admin_obj=Truck.objects.filter(id=truck_id,admin_id=admin_id)
#             serializer=FleetViewSerializer(admin_obj,many=True)
#             response_payload = {
#                 'is_authenticated': True,
#                 'status': status.HTTP_200_OK,
#                 'messages': "data updated succesfully",
#                 'result': serializer.data,
#                 'additional_data': {},
#             }
#             return Response(response_payload)
#         else:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "truck id not found",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#     def destroy(self,request):
#         admin_id=request.user.id
#         truck_id=request.GET.get('truck_id')
#         if not (admin_id and truck_id):
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "Please provide admin and truck id",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)
#         if Truck.objects.filter(id=truck_id,admin_id=admin_id).exists():
#             Truck.objects.filter(id=truck_id,admin_id=admin_id).update(is_deleted='True',avail_status='False',is_verified='False')
#             response_payload = {
#                 'is_authenticated': True,
#                 'status': status.HTTP_200_OK,
#                 'messages': "data deleted succesfully",
#                 'result': [],
#                 'additional_data': {},
#             }
#             return Response(response_payload)
#         else:
#             response_payload = {
#                     'is_authenticated': False,
#                     'status':status.HTTP_400_BAD_REQUEST,
#                     'messages': "id not found",
#                     'result': [],
#                     'additional_data': {},
#                     }
#             return Response(response_payload)

        
        

class VehicleTruckView(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        admin_id=request.user.id
        # print(admin_id)
        query_set=Truck.objects.filter(avail_status=True,admin_id=admin_id)
        serializer=VechicleTruckSerializer(query_set,many=Truck)
        response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': "Trucks fetched succesfully",
                'result': serializer.data,
                'additional_data': {},
            }
        return Response(response_payload)
    
class AddDriverView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def list(self,request):
        try:
            admin_user = User.objects.get(id=str(request.user),role='admin')
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Admin id not valid please provided valid id',
                'result':[] ,
                'additional_data': {},
            }
            return Response(response_payload)
        add_driver_obj=AddDriver.objects.filter(admin=admin_user,is_deleted=False)
        data=[]
        for driver_obj in add_driver_obj:
            try:
                driver_id=driver_obj.driver
                # print(driver_id)
                try:
                    truck_no=Truck.objects.filter(driver_id=driver_id).values_list('truck_no',flat=True).first()
                    # print(truck_no)
                except AttributeError:
                    truck_no = None
            except Truck.DoesNotExist():
                truck=None
            data.append({
                'driver_id':driver_obj.driver.id,
                'admin_id':driver_obj.admin.id,
                'first_name':driver_obj.driver.first_name,
                'last_name':driver_obj.driver.last_name,
                'mobile':driver_obj.driver.mobile,
                'country_code':driver_obj.driver.country_code,
                'image':driver_obj.driver.image.url,
                "address":driver_obj.driver.address,
                "city":driver_obj.driver.city,
                "state":driver_obj.driver.state,
                "zipcode":driver_obj.driver.zipcode,
                "password":driver_obj.driver.one_time_pwd,
                "driver_license_no":driver_obj.driver.driver_license_no,
                "vehicle_no":truck_no,
                "driver_status":driver_obj.driver.driver_status
            })
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages':'driver fetched succesfully',
                'result':data,
                'additional_data': {},
            }
        return Response(response_payload)
        
    def create(self, request):
        try:
            admin_user = User.objects.get(id=str(request.user),role='admin')
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Admin id not valid please provided valid id',
                'result':[] ,
                'additional_data': {},
            }
            return Response(response_payload)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        mobile = request.data.get('mobile')
        if not re.match("^\\d{9,13}$",mobile):
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'please enter a valid mobile number',
                'result':[] ,
                'additional_data': {},
            }
            return Response(response_payload)
        country_code = request.data.get('country_code')
        # vehile = request.data.get('vehile')
        address=request.data.get('address')
        # email = request.data.get('email')
        city=request.data.get('city')
        state=request.data.get('state')
        zipcode=request.data.get('zipcode')
        # gst = request.data.get('gst')        
        password = request.data.get('password')
        driver_license_no = request.data.get('driver_license_no')
        if driver_license_no:
            if User.objects.filter(driver_license_no=driver_license_no,is_deleted='False').exists():
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages':'this driver already exists',
                    'result':[] ,
                    'additional_data': {},
                }
                return Response(response_payload)
        elif not driver_license_no:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages':'Please enter your driving license number',
                    'result':[] ,
                    'additional_data': {},
                }
            return Response(response_payload)
        role=request.data.get('role')
        if not re.match("^\\d{9,13}$",mobile):
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Enter a valid mobile number',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not first_name:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your first name',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not last_name:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your last name',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your mobile number',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not country_code:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your country code ',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not address:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your address',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not city:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your city',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not state:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your state',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not zipcode:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your zip code',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not password:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter a password',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not driver_license_no:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please provide driving license number',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if User.objects.filter(mobile=mobile).exists():
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number already exists',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
            
        user_object = User()
        user_object.first_name=first_name
        user_object.last_name=last_name
        # user_object.set_password(password)
        user_object.mobile = mobile
        user_object.country_code = country_code
        user_object.role="driver"
        user_object.is_active=True
        user_object.city=city
        user_object.state=state
        user_object.zipcode=zipcode
        user_object.driver_license_no=driver_license_no
        user_object.address=address
        user_object.driver_status='Available'
        user_object.save()
        add_driver_obj=AddDriver()
        add_driver_obj.admin=admin_user
        add_driver_obj.driver=user_object
        add_driver_obj.status=True
        add_driver_obj.save()
        user_object.one_time_pwd=custom_send_otp(mobile,country_code,password)["otp"] 
        user_object.save()
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_201_CREATED,
            'messages': 'Driver registered Succesfully',
            'result': [],
            'additional_data': {},
        }
        return Response(response_payload)
    def update(self,request):
        admin_id=request.user.id
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        mobile = request.data.get('mobile')
        city=request.data.get('city')
        address=request.data.get('address')
        state=request.data.get('state')
        zipcode=request.data.get('zipcode')
        password = request.data.get('password')
        driver_license_no = request.data.get('driver_license_no')
        driver_id=request.data.get('driver_id')
        if not re.match("^\\d{9,13}$",mobile):
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'Enter a valid mobile number',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not driver_id:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter driver id',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not first_name:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your first name',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not last_name:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your last name',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your mobile number',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not address:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your address',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not city:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your city',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not state:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your state',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not zipcode:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter your zip code',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not password:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please enter a password',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not driver_license_no:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'please provide driving license number',
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        if not re.match("[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}",driver_id):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Enter a valid driver id",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload,status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(id=driver_id).exists():
            User.objects.filter(id=driver_id).update(first_name=first_name,last_name=last_name,mobile=mobile,address=address,city=city,
                                                     state=state,zipcode=zipcode,one_time_pwd=password,driver_license_no=driver_license_no)
            response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_201_CREATED,
                    'messages': "Driver details updated succesfully",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Driver id does not exist",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
    def destroy(self,request):
        driver_id=request.GET.get('driver_id')
        if not driver_id:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please provide driver id",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if User.objects.filter(id=driver_id,role='driver',is_deleted='False').exists():
            User.objects.filter(id=driver_id,role='driver').update(is_deleted='True')
            AddDriver.objects.filter(driver_id=driver_id).update(is_deleted='True',status='False')
            response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_201_CREATED,
                    'messages': "Driver removed succesfully",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        elif User.objects.filter(id=driver_id,is_deleted='True').exists():
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "driver already deleted",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "driver id not found",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
            
            

class AdminAccountView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)

    def create(self,request):
        # import pdb; pdb.set_trace()

        admin_id=request.user.id
        # print(admin_id)
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email=request.data.get('email')
        if not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email):
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "enter a valid email",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if User.objects.filter(email=email).exists():
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "email already exists",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        username=email.split("@")[0]
        mobile=request.data.get('mobile',None)
        if not re.match("^\\d{9,13}$",mobile):
            response_payload={
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "enter correct mobile number",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if User.objects.filter(mobile=mobile).exists():
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "mobile already exists",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        password=request.data.get('password',None)
        supervisor=User.objects.create(first_name=first_name,last_name=last_name,email=email,mobile=mobile,username=username,password=password,role='supervisor')
        supervisor_id=supervisor.id
        admin=AdminProfile.objects.create(user_id=supervisor_id)
        admin_instance=AdminAccounts.objects.create(supervisor_id=supervisor_id,admin_id=admin_id)
        response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages': "User added succesfully",
                'result': [],
                'additional_data': {},
            }
        return Response(response_payload)
    def list(self,request):
        admin_id=request.user.id
        admin=AdminAccounts.objects.filter(admin_id=admin_id)
        payload=[]
        active_supervisor=[y for y in admin if not y.supervisor.is_deleted]
        print(active_supervisor)
        for y in active_supervisor:
            # truck=Truck.objects.filter(id=active_supervisor.id)
            # print(truck)
            supervisor_id=y.supervisor.id
            truck=Truck.objects.filter(supervisor_id=supervisor_id)
            truck_name=[]
            for x in truck:
                truck_name.append({
                    'truck_no':x.truck_no
                })
            supervisor_name=[]
            for x in truck:
                try:
                    driver=x.driver.first_name
                except:
                    driver=None
                supervisor_name.append({
                    'driver':driver
                })
            # print(truck_name)
            payload.append({
            'first_name':y.supervisor.first_name,
            'last_name':y.supervisor.last_name,
            'email':y.supervisor.email,
            'mobile':y.supervisor.mobile,
            'username':y.supervisor.username,
            'role':y.supervisor.role,
            'supervisor_id':y.supervisor.id,
            'password':y.supervisor.password,
            'truck':truck_name,
            'driver':supervisor_name
        })
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "Data fetched succesfully",
            'result': payload,
            'additional_data': {},
        }
        return Response(response_payload)
    def update(self,request):
        admin_id=request.user.id
        supervisor_id=request.data.get('supervisor_id')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email=request.data.get('email',None)
        
        username=request.data.get('username')
        password=request.data.get('password')
        if not email:
            if not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email):
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "enter a valid email",
                    'result': [],
                    'additional_data': {},
                    }
                return Response(response_payload)
        if not email:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "email already exists",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        mobile=request.data.get('mobile',None)
        if not re.match("^\\d{9,13}$",mobile):
            response_payload={
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "enter correct mobile number",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
        User.objects.filter(id=supervisor_id).update(first_name=first_name,last_name=last_name,email=email,mobile=mobile,username=username,password=password)
        response_payload={
            'is_authenticated':True,
            'status':status.HTTP_200_OK,
            'messages':'Revamped and Renewed: User Successfully Upgraded!',
            'result': [],
            'additional_data':{}
        }
        return Response(response_payload)
    def destroy(self,request):
        supervisor_id=request.GET.get('supervisor_id')
        if User.objects.filter(id=supervisor_id,is_deleted='False').exists():
            user=User.objects.get(id=supervisor_id)
            user.is_deleted='True'
            user.save()
            AdminAccounts.objects.filter(supervisor_id=supervisor_id).update(is_deleted='True')
            response_payload={
            'is_authenticated':True ,
            'status':status.HTTP_200_OK,
            'messages':"Supervisor removed succesfully",
            'result': [],
            'additional_data':{}
        }
            return Response(response_payload)
        elif User.objects.filter(id=supervisor_id,is_deleted='True').exists():
            response_payload={
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Supervisor already deleted",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
class SupervisorView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        admin_id=request.user.id
        admin=AdminAccounts.objects.filter(admin_id=admin_id)
        payload=[]
        active_supervisor=[y for y in admin if not y.supervisor.is_deleted]
        for y in active_supervisor:
            payload.append({
            'first_name':y.supervisor.first_name,
            'last_name':y.supervisor.last_name,
            'supervisor_id':y.supervisor.id,
            'role':y.supervisor.role
        })
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': "Data fetched succesfully",
            'result': payload,
            'additional_data': {},
        }
        return Response(response_payload) 
    
from django.core.exceptions import ObjectDoesNotExist
class AdminResponseView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def create(self,request):
        admin_id=request.user.id 
        trip_id=request.data.get('trip_id')
        response=request.data.get('response')
        amount=request.data.get('amount')
        days=request.data.get('days')
        hours=request.data.get('hours')
        if not (trip_id and response and amount and days):
            response_payload={
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "Please specify all the details",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not hours:
            hours=0
        transit_time=int(days)*24 + int(hours)
        print(transit_time)
        try:
            trip_obj=Trip.objects.get(id=trip_id,trip_status='requested') 
        except ObjectDoesNotExist:
            response_payload={
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Response already submitted for this trip",
                'result': [],
                'additional_data': {},
                }
            return Response(response_payload) 
        if AdminResponse.objects.filter(admin_id=admin_id,trip_id=trip_id).exists():
            response_payload={
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "Response already submitted for this trip",
                'result': [],
                'additional_data': {},
                }
            return Response(response_payload)
        # trip_obj.trip_status='requested'
        trip_obj.admin_id=admin_id
        trip_obj.save()
        admin=AdminResponse.objects.create(admin_id=admin_id,trip_id=trip_id,response=response,
                                         proposed_amount=amount,transit_time=transit_time)
        response_payload={
            'is_authenticated':True,
            'status':status.HTTP_200_OK,
            'messages':"Response taken succesfully",
            'result':[],
            'additional_data':{}
            }
        return Response(response_payload)
        
            
class AdminTripView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        admin_id=request.user.id
        trip_status=request.GET.get('trip_status')
        trip_ids=Trip.objects.filter(admin_id=admin_id).values_list('id',flat=True)
        if trip_status=='requested':
            pay_load1=[]
            # for y in trip_ids:
            queryset = Trip.objects.filter(trip_status='requested').order_by('-created_at')
            for x in queryset:
                pay_load1.append({
                        'destination':x.destination,
                        'starting_point':x.starting_point,
                        'trip_id_show':x.trip_id_show,
                        'truck_type':x.truck_type,
                        'material_type':x.material.material_type,
                        'material_weight':x.submaterial.material_weight,
                        'submaterial':x.submaterial.material_subtype,
                        'starting_date':x.starting_date,
                        'starting_time':x.starting_time,
                        'trip_status':x.trip_status,
                        'trip_id':x.id,
                        'constraints':{"temprature":x.submaterial.temprature,"humidity":x.submaterial.humidity,"tilt":x.submaterial.tilt,"ambient_light":x.submaterial.ambient_light,"pitch_angle":x.submaterial.pitch_angle,"roll_angle":x.submaterial.roll_angle}
                    })
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages':"trip data fetched succesfully",
                'result':pay_load1,
                'additional_data': {}
                }
            return Response(response_payload)
        elif trip_status=='ongoing':
            pay_load=[]
            for y in trip_ids:
                queryset=Trip.objects.filter(id=y,trip_status='ongoing')
                for x in queryset:
                    try:
                        truck = x.truck
                        try: 
                            driver = truck.driver
                            driver_name = driver.first_name
                        except AttributeError:
                            driver_name = None
                        try:
                            truck_no = truck.truck_no 
                            tracker_id=truck.tracker_id
                        except AttributeError:
                            truck_no = None
                            tracker_id=None
                    except Truck.DoesNotExist:
                        driver_name = None
                        truck_no = None
                        tracker_id=None
                    pay_load.append({
                        'trip_id':x.id,
                        "tracker_id":tracker_id,
                        'truck_number':truck_no,
                        'source':x.starting_point,
                        'destination':x.destination,
                        'trip_id_show':x.trip_id_show,
                        'starting_date':x.starting_date,
                        'starting_time':x.starting_time,
                        'driver':driver_name,
                        'status':x.trip_status
                    })
                
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages':"trip data fetched succesfully",
                'result':pay_load,
                'additional_data': {}
                }
            return Response(response_payload)
                    
        elif trip_status=='upcoming':
            pay_load=[]
            for y in trip_ids:
                queryset=Trip.objects.filter(id=y,trip_status='upcoming')
                for x in queryset:
                    try:
                        truck = x.truck
                        try: 
                            driver = truck.driver
                            driver_name = driver.first_name
                        except AttributeError:
                            driver_name = None
                        try:
                            truck_no = truck.truck_no 
                        except AttributeError:
                            truck_no = None
                    except Truck.DoesNotExist:
                        driver_name = None
                        truck_no = None
                    pay_load.append({
                        'trip_id':x.id,
                        'truck_number':truck_no,
                        'trip_id_show':x.trip_id_show,
                        'source':x.starting_point,
                        'destination':x.destination,
                        'starting_date':x.starting_date,
                        'starting_time':x.starting_time,
                        'driver':driver_name
                    })
                
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages':"trip data fetched succesfully",
                'result':pay_load,
                'additional_data': {}
                }
            return Response(response_payload)
        elif trip_status=='completed':
            pay_load=[]
            for y in trip_ids:
                queryset=Trip.objects.filter(id=y,trip_status='completed')
                for x in queryset:
                    try:
                        truck = x.truck
                        try: 
                            driver = truck.driver
                            driver_name = driver.first_name
                        except AttributeError:
                            driver_name = None
                        try:
                            truck_no = truck.truck_no 
                        except AttributeError:
                            truck_no = None
                    except Truck.DoesNotExist:
                        driver_name = None
                        truck_no = None
                    pay_load.append({
                        'trip_id':x.id,
                        'truck_number':truck_no,
                        'trip_id_show':x.trip_id_show,
                        'source':x.starting_point,
                        'destination':x.destination,
                        'starting_date':x.starting_date,
                        'starting_time':x.starting_time,
                        'end_date':[x.driver_trip_complete_date.strftime('%d/%m/%Y,%I:%M %p') if  x.driver_trip_complete_date is not None else ""][0],
                        'driver':driver_name,
                    })        
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages':"trip data fetched succesfully",
                'result':pay_load,
                'additional_data': {}
                }
            return Response(response_payload)   
        else:
            response_payload = {    
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages':"enter a valid trip type",
                'result':[],
                'additional_data': {}
                }
            return Response(response_payload)

class AssignTripView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def create(self,request):
        # import pdb; pdb.set_trace()
        admin_id=request.user.id
        trip_id=request.data.get('trip_id')
        truck_id=request.data.get('truck_id')
        if not trip_id:
            response_payload = {    
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages':"Invalid Trip id",
                'result':[],
                'additional_data': {}
                }
            return Response(response_payload) 
        try:
            Truck.objects.filter(id=truck_id,admin_id=admin_id,avail_status='True')
        except:
            response_payload = {    
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages':"Invalid truck id",
                'result':[],
                'additional_data': {}
                }
            return Response(response_payload) 
        try:
            truck=Truck.objects.get(id=truck_id)
            driver_id=truck.driver.id
        except:
            driver_id=None
        if Trip.objects.filter(id=trip_id).exists():
            try:
                existing_truck = Trip.objects.filter(id=trip_id).first()

                if existing_truck:
                    existing_truck_id = existing_truck.truck
                    # print(existing_truck_id.id)
                    try:
                        Truck.objects.filter(id=existing_truck_id.id).update(avail_status=True)
                    except:
                        pass
            except:
                pass
            Trip.objects.filter(id=trip_id).update(truck_id=truck_id)
            Truck.objects.filter(id=truck_id).update(avail_status=False)
            try:
                driver = User.objects.filter(id=driver_id).values('fcm_token')
                # print(driver)
                fcm_tokens = [item['fcm_token'] for item in driver] 
                # print(fcm_tokens)
                firebase_object=FirePushNotication.objects.filter(fire_type='Trip start notification', role='driver').last()
                # print(firebase_object)
                send_notification(fcm_tokens, firebase_object.title , firebase_object.description)
                print("Notification sent to driver")
            except:
                pass
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages':"Truck assigned succesfully",
                'result':[],
                'additional_data': {}
                }
            return Response(response_payload) 
        else:
            response_payload = {    
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages':"Invalid Trip id",
                'result':[],
                'additional_data': {}
                }
            return Response(response_payload) 
class AdminPaymentView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        # import pdb; pdb.set_trace()
        admin_id=request.user.id 
        if Trip.objects.filter(admin_id=admin_id).exists():
            trip_obj=Trip.objects.filter(admin_id=admin_id)
            serializer=PaymentStatusSerializer(trip_obj,many=True)
            response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages':"payment status fetched succesfully",
                    'result':serializer.data,
                    'additional_data': {}
                    }
            return Response(response_payload)
        else:
            response_payload = {    
                    'is_authenticated': False,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'messages':"No trip found for this id",
                    'result':[],
                    'additional_data': {}
                    }
            return Response(response_payload)
class TrackerListView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        admin_id=request.user.id 
        # print(admin_id)
        if TrackerDeviceInfo.objects.filter(admin_id=admin_id).exists():
            tracker_list=TrackerDeviceInfo.objects.filter(admin_id=admin_id,tracker_assigned='False').values('device','tracker_assigned')
            response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages':"tracker list fetched succesfully",
                    'result':tracker_list,
                    'additional_data': {}
                    }
            return Response(response_payload)
        else:
            response_payload = {    
                    'is_authenticated': False,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'messages':"No tracker associated with your id",
                    'result':[],
                    'additional_data': {}
                    }
            return Response(response_payload)
class Tracker_location(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    # pagination_class = PageNumberPagination
    def list(self, request):
        id=request.user.id
        trip_id=request.GET.get('trip_id')
        lst=[]
        datetimeoftrip=datetime(2023, 4, 4, 12, 55, 59, 342380)
        if Trip.objects.filter(id=trip_id, trip_status='ongoing', admin_id=id).exists():
            x=Trip.objects.filter(id=trip_id)
            for i in x:
                if i.truck_id is not None:
                    tracker_id=i.truck.tracker_id
                else:
                    response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Truck details do not exist for this user.',
                    }
                    return Response(response_payload)
        else:
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Trip do not exist for this user or has not started yet.',
                    }
            return Response(response_payload)
        if not tracker_id:
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Tracker ID not found for this vehicle.',
                    }
            return Response(response_payload)
        gmaps = googlemaps.Client(key='AIzaSyDJraB9ewkAmyzoN_Q4lkh4Tw3m_hShXOU')
        current_time=datetime.now()
        # print(current_time)
        info = TrackerDeviceIntergrations.objects.filter(device=tracker_id, type='GPS Data')
        after_time=datetime.now()
        print(after_time)
        lst = []

        for x in info:
            diff = datetime.now() - x.created_at

            # if datetimeoftrip < x.created_at <= datetime.now():
            #     Latitude = x.latitude
            #     Longitude = x.longitude
                
                # Geocode the coordinates using Google Maps
                # geocode_result = gmaps.reverse_geocode((Latitude, Longitude))
                
                # if geocode_result:
                #     address = geocode_result[0]['formatted_address']
                #     created_at = x.created_at.strftime('%Y-%m-%d,%H:%M:%S')

            lst.append( {
                        'id': x.id,
                        'Longitude': x.longitude,
                        'Latitude': x.latitude,
                        'tracker_id':tracker_id
                    })

                    # merged = {'address': address, **payload}
            # lst.append(payload)
                # else:
                #     response_payload = {
                #         'is_authenticated': False,
                #         'status': status.HTTP_404_NOT_FOUND,
                #         'messages': 'Location details not found.',
                #     }
                #     return Response(response_payload)
            # else:
            #     response_payload = {
            #         'is_authenticated': False,
            #         'status': status.HTTP_404_NOT_FOUND,
            #         'messages': 'Location details not found.',
            #     }
            #     return Response(response_payload)
        
        response_payload = {
            'is_authenticated': True,
            'status': status.HTTP_200_OK,
            'messages': 'Following are the location details',
            'result': lst,
        }

        return Response(response_payload)
    
class TrackerLocationView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    # pagination_class = PageNumberPagination
    def list(self, request):
        id=request.user.id
        trip_id=request.GET.get('trip_id')
        trip_status=request.GET.get('trip_status')
        if trip_status=="ongoing":
            try:
                trip_obj=Trip.objects.get(id=trip_id,trip_status=trip_status)
            except Exception as e:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': 'Trip id does not exist',
                    'result': {},
                    'additional_data': {},
                }
                return Response(response_payload)
            
            trip_serializer= TripOngoingSerializer(trip_obj)
            trip_data=trip_serializer.data
            tracker_trip_data=TrackerDeviceIntergrations.objects.filter(trip_id=trip_id,type="GPS Data").order_by('-id')
            trakcer_serializer=TrackerDeviceIntergrationsAdminLocationSerializer(tracker_trip_data,many=True)
            trakcer_serializer_data=trakcer_serializer.data
            trip_data['trip']=trakcer_serializer_data
            response_payload={
                        'is_authenticated': True,
                        'status':status.HTTP_200_OK,
                        'messages': "Real-time tracking of location data",
                        'result':trip_data,
                        'additional_data': {},
                        }
            return Response(response_payload)
        elif trip_status=="completed":
            try:
                trip_obj=Trip.objects.get(id=trip_id,trip_status=trip_status)
            except Exception as e:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': 'Trip id does not exist',
                    'result': {},
                    'additional_data': {},
                }
                return Response(response_payload)
            
            trip_serializer= TripOngoingSerializer(trip_obj)
            trip_data=trip_serializer.data
            tracker_trip_data=TrackerDeviceIntergrations.objects.filter(trip_id=trip_id,type="GPS Data")
            trakcer_serializer=TrackerDeviceIntergrationsAdminLocationSerializer(tracker_trip_data,many=True)
            trakcer_serializer_data=trakcer_serializer.data
            trip_data['trip']=trakcer_serializer_data
            response_payload={
                        'is_authenticated': True,
                        'status':status.HTTP_400_BAD_REQUEST,
                        'messages': "Trip successfully finished.",
                        'result':trip_data,
                        'additional_data': {},
                        }
            return Response(response_payload)
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': 'Trip id does not exist',
                    'result': {},
                    'additional_data': {},
                }
            return Response(response_payload)
            
        
    
    
class DriverListView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        admin_id=request.user.id
        driver=AddDriver.objects.filter(admin=admin_id,status=True,is_deleted='False')
        payload=[]
        for x in driver:
            payload.append({
                'driver_id':x.driver.id,
                'first_name':x.driver.first_name,
                'last_name':x.driver.last_name,
                'driver_status':x.status
            })
        response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages':"driver list fetched succesfully",
                    'result':payload,
                    'additional_data': {}
                    }
        return Response(response_payload)
class HelpDeskView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def create(self,request):
        admin_id=request.user.id
        query=request.data.get('query')
        if not query:
            response_payload = {    
                    'is_authenticated': False,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'messages':"Please specify your query",
                    'result':[],
                    'additional_data': {}
                    }
            return Response(response_payload)
        HelpDeskQuery.objects.create(admin_id=admin_id,query=query)
        response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages':"Your query submitted succesfully will respond to it soon",
                    'result':[],
                    'additional_data': {}
                    }
        return Response(response_payload)
        
    
class PagePagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_size = 3
    
from adminapp.api.pagination import CustomPagination

class TrackerHistoryAdminView(generics.GenericAPIView):
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAllSerializer
    # pagination_class = CustomPagination
    def get(self, request):
        deviceid=request.GET.get('deviceid')
        queryset = TrackerDeviceIntergrations.objects.filter(device=deviceid).order_by('-id')
        serializer=TrackerDeviceIntergrationAllSerializer(queryset,many=True)
        # page = request.GET.get('offset')
        # if page is not None:
        #     page = self.paginate_queryset(queryset)
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        # serializer = self.serializer_class(queryset, many=True)
        data=serializer.data
        response_payload = {
            'is_authenticated': True,
            'status':status.HTTP_200_OK,
            'messages': "Successful access to historical data.",
            'result': data,
            'additional_data': {},
           }
        return Response(response_payload)
       
    
class TrackerDeviceAdminDetails(generics.GenericAPIView):
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAllSerializer
   
    def get(self, request):
        deviceid=request.GET.get('deviceid')
        if not deviceid:
            response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': 'Device ID does not exist',
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        try:
            queryset = TrackerDeviceIntergrations.objects.filter(device=deviceid).order_by('-id')[0]
        except:
            response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': 'Device ID does not exist',
                'result': {},
                'additional_data': {},
            }
            return Response(response_payload)
        
        serializer = TrackerDeviceIntergrationAllSerializer(queryset)
        pay_load=serializer.data
        response_payload = {
        'is_authenticated': True,
        'status': status.HTTP_200_OK,
        'messages': "Device details successfull",
        'result': pay_load,
        'additional_data': {},
        }
        return Response(response_payload)
    
    
class AdminTrackerListView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        admin_id=request.user.id 
        print(admin_id)
        if TrackerDeviceInfo.objects.filter(admin_id=admin_id).exists():
            tracker_list=TrackerDeviceInfo.objects.filter(admin_id=admin_id).values('device','tracker_assigned','firmware_version','hardware_version','serial_no')
            response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages':"tracker list fetched succesfully",
                    'result':tracker_list,
                    'additional_data': {}
                    }
            return Response(response_payload)
        else:
            response_payload = {    
                    'is_authenticated': False,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'messages':"No tracker associated with your id",
                    'result':[],
                    'additional_data': {}
                    }
            return Response(response_payload)
        
class AllDeviceLocationView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    pagination_class = PageNumberPagination
    def list(self,request):
        id=request.user.id 
        trip_ids=Trip.objects.filter(admin_id=id,trip_status='ongoing').values_list('id',flat=True)[:10]
        print(trip_ids)
        payload1=[]
        lst=[]
        mst=[]
        for y in trip_ids:
            print('yyyyyyy',y)
                # print(y)
        #print(trip_id)
            datetimeoftrip=datetime(2023, 4, 4, 12, 55, 59, 342380)
        #print(datetimeoftrip)
            
            if Trip.objects.filter(id=y, trip_status='ongoing', admin_id=id).exists():
                # lst=[]
                x=Trip.objects.filter(id=y, trip_status='ongoing', admin_id=id)
                print('x',x)
                for i in x:
                    if i.truck_id is not None:
                        tracker_id=i.truck.tracker_id
                        #print(tracker_id)
                    else:
                        response_payload = {
                            
                            'is_authenticated': False,
                            'status': status.HTTP_404_NOT_FOUND,
                            'messages': 'Truck details do not exist for this user.',
                        }
                        return Response(response_payload)

            else:
                response_payload = {
                            
                            'is_authenticated': False,
                            'status': status.HTTP_404_NOT_FOUND,
                            'messages': 'Trip do not exist for this user or has not started yet.',
                        }
                return Response(response_payload)
            if not tracker_id:
                response_payload = {
                            
                            'is_authenticated': False,
                            'status': status.HTTP_404_NOT_FOUND,
                            'messages': 'Tracker ID not found for this vehicle.',
                        }
                return Response(response_payload)
            # gmaps = googlemaps.Client(key='AIzaSyDJraB9ewkAmyzoN_Q4lkh4Tw3m_hShXOU')
            data=None
            try:
                info=TrackerDeviceIntergrations.objects.filter(trip_id=y, type='GPS Data')
            except:
                if len(info)==0:
                    data=None
            # if data:
            for x in info:
                diff = datetime.now() - x.created_at
                if datetimeoftrip < x.created_at <= datetime.now():
                    created_at = x.created_at.strftime('%Y-%m-%d,%H:%M:%S')
                    lst.append({
                        'id': x.id,
                        'Longitude': x.longitude,
                        'Latitude': x.latitude,
                        'created_at': created_at,
                        'tracker_id':tracker_id
                    })
                    lat_long = [{k: v for k, v in d.items() if k in ('Latitude', 'Longitude')} 
            for d in lst]
                    data=lat_long
                # else:
                #     response_payload = {
                            
                #             'is_authenticated': False,
                #             'status': status.HTTP_404_NOT_FOUND,
                #             'messages': 'location details not found.',
                #         }
                #     return Response(response_payload)
            queryset=Trip.objects.filter(id=y,trip_status='ongoing')[:10]
            try:
                address=TrackerDeviceIntergrations.objects.filter(trip_id=y).values_list('address',flat=True).last()
                # print(address)
            except:
                address=None
            if data is not None:
                for x in queryset:
                    payload1.append({
                        'trip_id':x.id,
                        'lat_long':data[-1],
                        'truck_no':x.truck.truck_no,
                        'truck_id':x.truck.id,
                        'address':address
                    })
            elif data==None:
                payload1==None
        response_payload = {                   
                        'is_authenticated': True,
                        'status': status.HTTP_200_OK,
                        'messages': 'following are the locations details',
                        'result': payload1,            
                    }
        return Response(response_payload)

    
class AdminAlertTripView(viewsets.ViewSet):
    queryset = TrackerDeviceIntergrations.objects.all()
    serializer_class = TrackerDeviceIntergrationAlertSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request):
        deviceid=request.GET.get('deviceid')
        if not deviceid:
            response_payload = {
            'is_authenticated': False,
            'status':status.HTTP_400_BAD_REQUEST,
            'messages': "Get method is not allowed",
            'result': [],
            'additional_data': {},
           }
            return Response(response_payload)
        try:
            queryset = TrackerDeviceIntergrations.objects.filter(device=deviceid.upper(),type='Alert Data').order_by('-id')
        except Exception as e:
            response_payload = {
            'is_authenticated': False,
            'status':status.HTTP_400_BAD_REQUEST,
            'messages': "Tracker id does not exist",
            'result': [],
            'additional_data': {},
            }
            return Response(response_payload)     
        if queryset is not None:
            
            serializer = TrackerDeviceIntergrationAlertSerializer(queryset,many=True)
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
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)

class TruckCountView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        admin_id=request.user.id
        avail_truck=Truck.objects.filter(avail_status=True,admin_id=admin_id,is_deleted='False') 
        occupy_truck=Truck.objects.filter(avail_status=False,admin_id=admin_id,is_deleted='False')
        if any([avail_truck, occupy_truck]):
            payload={'available_count':avail_truck.count(),
                    'occupied_truck':occupy_truck.count()}
            response_payload = {
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages': "Truck count fetched succesfully",
                    'result': payload,
                    'additional_data': {},
                }
            return Response(response_payload) 
        else:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "No trucks available",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        
class LocationBasedTrackerView(viewsets.ViewSet):
    permission_classes=(AllowAny,)
    def list(self,request):
        tracker_id=request.GET.get('tracker_id')
        if not tracker_id:
            response_payload = {
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Please enter the tracker id',
                        'result': [],
                        'additional_data': {},
                    }
            return Response(response_payload)
        tracker_obj=TrackerDeviceIntergrations.objects.filter(device=tracker_id, type='GPS Data').last()
        tracker_serilizer=TrackerDeviceIntergrationsAdminDetailSerializer(tracker_obj)
        data=tracker_serilizer.data
        response_payload = {                   
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages': 'following are the locations details',
                    'result': data,           
                }
        return Response(response_payload)
        