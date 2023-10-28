from django.forms import ValidationError
from django.shortcuts import render
import googlemaps
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import exceptions
from customer.models import User,MobileOTP,Profile,FirePushNotication
import jwt,requests,re,random
from rest_framework import status, generics
from rest_framework import viewsets
from customer.config import *
from customer.helpers import *
from datetime import datetime,timedelta
import random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,RefreshToken
from django.core.mail import send_mail
from TrackerApp.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
import socket
from django.shortcuts import get_object_or_404
from customer.api.serializers import ViewvendorlistSerializer,PaymentHistorySerializer,UpdateKYCSerializer,ViewaddressbookSerializer,Trackerdeviceintegrations,Coupon_Serializer,TruckSerializer_vendor,TruckSerializer,OrganizationSerializer,MaterialSerializer,GetQuoteSerializer,TruckIDWithTrackerIDSerializer,NotificationSerializer, UpdateProfileSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
import razorpay
from adminapp.models import Truck, Trip, AdminResponse, AdminProfile
from driverapp.models import TrackerDeviceIntergrations
import time
# from adminapp.models import TrackerDeviceIntergrations
from django.views.decorators.csrf import csrf_exempt
#import reverse_geocode
from geopy.geocoders import Nominatim
from customer.api.sendmobileotp import send_otp
from PIL import Image
from utils.views import post_meridiem_time
import io
from django.core.files.images import ImageFile
from django.db import IntegrityError
# Imports for PDF
from django.http import FileResponse
import io # input output
from reportlab.pdfgen import canvas # will put all the data in canvas and save it as pdf
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from driverapp.api.base64 import base64_file
from datetime import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files.base import ContentFile
from adminapp.api.serializers import TripOngoingSerializer,TrackerDeviceIntergrationsAdminLocationSerializer
from django.db.models import Q

# import geocoder
# class CreateOTPView(viewsets.ViewSet):
#     def create(self, request):
#         mobile = request.data.get('mobile')
#         country_code = request.data.get('country_code')
#         type = request.data.get('type')
#         fcm_token=request.data.get('fcm_token')
#         if not mobile:
#             response_payload = {
#                 'is_authenticated': False,
#                 'status':status.HTTP_400_BAD_REQUEST,
#                 'messages': 'mobile number not provided',
#                 'result': 'otp not created',
#                 'additional_data': {},
#             }
#             return Response(response_payload)
#         if not country_code:
#             response_payload = {
#                 'is_authenticated': False,
#                 'status':status.HTTP_400_BAD_REQUEST,
#                 'messages': 'country code not provided',
#                 'result': 'otp not created',
#                 'additional_data': {},
#             }
#             return Response(response_payload)            
#         user_object,created = User.objects.get_or_create(mobile=mobile)
#         user_object.fcm_token=fcm_token
#         user_object.role='customer'
#         user_object.save()
#         if user_object.type=='Organization':
#             if user_object.mobile==mobile:
#                     # user_object.fcm_token=fcm_token
#                     otp_object,created =MobileOTP.objects.get_or_create(user=user_object)
#                     otp_object.mobile=mobile
#                     otp_object.otp=send_otp(mobile,country_code)["otp"]
#                     otp_object.time=int(float((datetime.now().timestamp())))
#                     otp_object.save()
#                     resp = {
#                 'is_authenticated': True,
#                 'status':status.HTTP_201_CREATED,
#                 'message':'Organizationn logged in succesfully',
#                 'result': '',
#                 'additional_data': {},
#                 }
#                     return JsonResponse(resp)
#         else:    
#             user_object.country_code=country_code
#             user_object.type=type
#             user_object.mobile=mobile
#             user_object.fcm_token=fcm_token
#             user_object.role='customer'
#             user_object.save()
#             profile, created = Profile.objects.get_or_create(user=user_object)
#             profile.save()
#             user_object.save()
#             otp_object,created =MobileOTP.objects.get_or_create(user=user_object)
#             otp_object.mobile=mobile
#             otp_object.otp=send_otp(mobile,country_code)["otp"]  
#             otp_object.time=int(float((datetime.now().timestamp())))
#             otp_object.save()
#             response_payload = {
#             'is_authenticated': True,
#             'status': status.HTTP_201_CREATED,
#             "mobile_no":str(user_object.mobile),
#             'messages': 'OTP send succesfully on your registared mobile number',
#             'result': [],
#             'additional_data': {},
#             }
#             return Response(response_payload)
    

class CreateOTPView(viewsets.ViewSet):
    def create(self, request):
        mobile = request.data.get('mobile')
        country_code = request.data.get('country_code')
        type = request.data.get('type')
        fcm_token=request.data.get('fcm_token')
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number not provided',
                'result': 'otp not created',
                'additional_data': {},
            }
            return Response(response_payload)
        if not country_code:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'country code not provided',
                'result': 'otp not created',
                'additional_data': {},
            }
            return Response(response_payload)            
        user_object,created = User.objects.get_or_create(mobile=mobile, role='customer')
        print(user_object)
        print(user_object.type)
        user_object.fcm_token=fcm_token
        user_object.role='customer'
        user_object.save()
        print(user_object.type)

        if type=='Organization' and user_object.type!='Organization':
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'This user do not exist',
                'result': 'This user do not exist',
                'additional_data': {},
            }
            return Response(response_payload)


        if user_object.type=='Organization' :
            if type=='Organization':
                if user_object.mobile==mobile:
                        # user_object.fcm_token=fcm_token
                        otp_object,created =MobileOTP.objects.get_or_create(user=user_object)
                        otp_object.mobile=mobile
                        otp_object.otp=send_otp(mobile,country_code)["otp"]
                        otp_object.time=int(float((datetime.now().timestamp())))
                        otp_object.save()
                        resp = {
                    'is_authenticated': True,
                    'status':status.HTTP_201_CREATED,
                    'message':'OTP sent successfully on your registered mobile number',
                    'result': '',
                    'additional_data': {},
                    }
                        return JsonResponse(resp)
            else:
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'This number is already registered as Organization',
                'result': 'This number is already registered as Organization',
                'additional_data': {},
            }
            return Response(response_payload)

        else :    
            if type=='Individual':
                user_object.country_code=country_code
                user_object.type=type
                user_object.mobile=mobile
                user_object.fcm_token=fcm_token
                user_object.role='customer'
                user_object.save()
                profile, created = Profile.objects.get_or_create(user=user_object)
                profile.save()
                user_object.save()
                otp_object,created =MobileOTP.objects.get_or_create(user=user_object)
                otp_object.mobile=mobile
                otp_object.otp=send_otp(mobile,country_code)["otp"]  
                otp_object.time=int(float((datetime.now().timestamp())))
                otp_object.save()
                response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                "mobile_no":str(user_object.mobile),
                'messages': 'OTP send succesfully on your registered mobile number',
                'result': [],
                'additional_data': {},
                }
                return Response(response_payload)
        
            else:
                response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'This number is already registered as Individual',
                'result': 'This number is already registered as Individual',
                'additional_data': {},
            }
                return Response(response_payload)
            



class VerifyOTPView(viewsets.ViewSet):
    def create(self, request):
        otp = request.data.get('otp')
        mobile = request.data.get('mobile')
        if not mobile:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number not provided',
                'result': 'otp not verified',
                'additional_data': {},
            }
            return Response(response_payload)
        if not otp:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'otp not provided',
                'result': 'otp not verified',
                'additional_data': {},
            }
            return Response(response_payload)
        try:
            user = User.objects.get(mobile=mobile)
        except:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages':'Mobile number not valid',
                'result':[] ,
                'additional_data': {},
            }

            return Response(response_payload)
        refresh_token=RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        refresh_token = str(refresh_token)        
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
                data={
                    "user_id":user.id,
                    "type":user.type,
                    "language_type":user.language_type,
                    "mobile_no":str(user.country_code)+"|"+str(user.mobile),
                    'access_token': access_token,
                    'refresh_token': refresh_token,                    
                    
                }
                response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    "messages":"Login Successful",
                    'result': data,
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

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            try:
                refresh_token = request.COOKIES["authentication_key"]
            except:
                response_payload = {
                    'is_authenticated': True,
                    'status': True,
                    'messages': {'logout': 'User not authenticated!'},
                    'result': 'Success!',
                    'additional_data': {},
                }
                return Response(response_payload, status=status.HTTP_401_UNAUTHORIZED)

            token = RefreshToken(refresh_token)
            token.blacklist()
            response_payload = {
                'is_authenticated': True,
                'status': True,
                'messages': {'logout': 'Logged out successfully!'},
                'result': 'Success!',
                'additional_data': {},
            }
            response_object = Response(response_payload, status=status.HTTP_200_OK)
            response_object.delete_cookie('authentication_key')
            response_object.delete_cookie('auth')
            return response_object
        except Exception as e:
            response_payload = {
                'is_authenticated': True,
                'status': True,
                'messages': [],
                'result': 'Success!',
                'additional_data': {},
            }
            return Response(response_payload, status=status.HTTP_401_UNAUTHORIZED)
        


class OrganizationView(APIView):
    def post(self,request):
        name = request.data.get('name')
        organization_name= request.data.get('organization_name')
        email = request.data.get('email')
        mobile= request.data.get('mobile')
        pan= request.data.get('pan')
        gst= request.data.get('gst')
        type= request.data.get('type')
        country_code = request.data.get('country_code')

        if not re.fullmatch("[A-Za-z]{2,25}( [A-Za-z]{2,25})?",name):
            return JsonResponse({'messages':'name should be alphabet only'})
        if not re.fullmatch("[A-Za-z]{2,25}( [A-Za-z]{2,25})?",organization_name):
            return JsonResponse({'messages':'name should be alphabet only'})
        if not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email):
            return JsonResponse({'messages':'email not valid'})
        if not re.match("^\\d{9,13}$",mobile):
            return JsonResponse({'messages':'number is not valid'})
        if not re.match("^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$",gst):
            return JsonResponse({'messages':'enter a valid gst'})
        if not re.match("[A-Za-z]{5}\d{4}[A-Za-z]{1}",pan):
            return JsonResponse({'messages':'enter a valid pan number'})
        if User.objects.filter(mobile=mobile).exists():
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number or email already exists',
                'result': 'user not registered',
                'additional_data': {},
            }
            return Response(response_payload)
        if User.objects.filter(email=email).exists():
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': 'mobile number or email already exists',
                'result': 'user not registered',
                'additional_data': {},
            }
            return Response(response_payload)
        user=User.objects.create(email=email,mobile=mobile,type=type, role='customer', country_code=country_code)
        print(user)
        org = Organization.objects.create(name=name,organization_name=organization_name ,pan=pan,gst=gst,user=user)
        subject="User registered succesfully"
        message="dear customer thanks for registering"
        htnl_message=render_to_string('email.html',{'context':'values'})
        recipent_list=[email]
        send_mail(subject,message,EMAIL_HOST_USER,recipent_list,html_message=htnl_message,fail_silently=False)
        # user.save()
        org.save()
        serializer_data=OrganizationSerializer(org)
        pay_load=serializer_data.data
        respone_payload={
            'is_authenticated': True,
            'status': status.HTTP_201_CREATED,
            'message': 'User registered successfully.',
            'result': pay_load,
            'additional_data': {}
        }
        return Response(respone_payload)
        
class TruckTypeView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def get(self, request):
        trucks=Truck.objects.filter(is_deleted='False').distinct('type')
        paginated_truck = self.pagination_class().paginate_queryset(trucks, request)
        serializer = TruckSerializer(paginated_truck,many=True)
        response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': 'following types of trucks are available',
                'truck_types': serializer.data,
            }
        return Response(response_payload)


class VendorlistView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def list(self, request):
        id=request.user.id
        trip_id=request.GET.get('trip_id')
        #print(trip_id)
        if not trip_id or not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",trip_id):
            response_payload = {
                'status':status.HTTP_401_UNAUTHORIZED,
                'messages': 'Valid Trip ID not found',
            }
            return Response(response_payload)
        name = Trip.objects.values('id')
        #print(name)
        for x in name:
            print(x['id'])
            if str(trip_id) == str(x['id']):
                queryset = Trip.objects.filter(user_id=id,id=trip_id)
                #print(queryset)
                
                for x in queryset:
                    truck_type=x.truck_type
                    starting_point=x.starting_point
                    destination=x.destination
                    starting_date=x.starting_date
                    # print(truck_type)
                    # print(starting_point)
                    # print(destination) 
                    trucks=Truck.objects.filter(type=truck_type, location=starting_point, avail_status=True)
                    paginated_truck = self.pagination_class().paginate_queryset(trucks, request)
                    serializer = TruckSerializer_vendor(trucks,many=True)
                    json_str=json.dumps(serializer.data)
                    regular_dict = json.loads(json_str)
                    for i in regular_dict:
                        i['Amount']="2000"
                        i['Starting_Date']=starting_date
                        i['Starting_point']=starting_point
                        i['Destination']=destination
                        i['Constraints']={"temprature":x.submaterial.temprature,"humidity":x.submaterial.humidity,"tilt":x.submaterial.tilt,"ambient_light":x.submaterial.ambient_light,"pitch_angle":x.submaterial.pitch_angle,"roll_angle":x.submaterial.roll_angle}
                    response_payload = {
                            'is_authenticated': True,
                            'status': status.HTTP_200_OK,
                            'messages': 'following vendors are available',
                            'vendor_list': regular_dict,             
                        }
                    return Response(response_payload)
        
        response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'messages': 'No vendor found',
            }
        return Response(response_payload)


class VendorlistView_new(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def list(self, request):
        id=request.user.id
        trip_id=request.GET.get('trip_id')
        print(trip_id)
        if not trip_id or not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",trip_id):
            response_payload = {
                'status':status.HTTP_401_UNAUTHORIZED,
                'messages': 'Valid Trip ID not found',
            }
            return Response(response_payload)
        queryset=AdminResponse.objects.filter(trip_id=trip_id).exclude(Q(response='declined') | Q(customer_response='declined'))
        print(queryset)
        payload=[]
        for x in queryset:
            payload.append({
                'source':x.trip.starting_point,
                'destination':x.trip.destination,
                'starting_date':x.trip.starting_date,
                'starting_time':x.trip.starting_time,
                'id':x.id,
                'response':x.response,
                'admin_id':x.admin_id,
                'trip_id':x.trip_id,
                'amount':x.proposed_amount,
                'transit_time':x.transit_time
            })
            
        print("@@@@@@@@@@@",payload)
        print(type(payload))
          
        response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages':"Following is the vendor list.",
                'result':payload,
                'additional_data': {}
            }
        return Response(response_payload)



class TrackIdWIthTrackerView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def get(self, request):
        trucks=Truck.objects.all()
        paginated_truck = self.pagination_class().paginate_queryset(trucks, request)
        serializer = TruckIDWithTrackerIDSerializer(paginated_truck,many=True)
        response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': 'following trucks  are  available here realted to trakcer',
                'truck_types': serializer.data,
            }
        return Response(response_payload)
class MaterailTypeView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        id=request.GET.get('id')        
        subtype_id=request.GET.get('subtype_id')
        print(subtype_id)
        type=Material.objects.filter(is_active=True)
        serializer = MaterialSerializer(type,many=True)
        if Material.objects.filter(id=id,is_active=True).exists():
            if MaterialSubtype.objects.filter(id=subtype_id).exists():
                constraints=MaterialSubtype.objects.filter(id=subtype_id).values('temprature','humidity','ambient_light','pitch_angle','roll_angle','tilt')
                response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': 'Success',
                'constraints':constraints,
            }
                return Response(response_payload)
            subtypes=MaterialSubtype.objects.filter(material_id=id).values('id','material_subtype')
            response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': 'Success',
                'material_subtype':subtypes,
            }
            return Response(response_payload)
        response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': 'Succsess',
                'material_types': serializer.data,
            }
        return Response(response_payload)
class GetQouteView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        id=request.user.id
        queryset=Trip.objects.all()
        serializer = GetQuoteSerializer(data=request.data)
        if serializer.is_valid():
            starting_date=serializer.validated_data.get('starting_date')
            if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",starting_date):
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid starting date",
                    'result': [],
                    'additional_data': {},
                    }
                return Response(response_payload)
            if not starting_date:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter a valid starting date",
                    'result': [],
                    'additional_data': {},
                    }
                return Response(response_payload)
            starting_time=serializer.validated_data.get('starting_time')
            if not starting_time:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please enter the starting time of trip",
                    'result': [],
                    'additional_data': {},
                    }
                return Response(response_payload)
            material_weight=serializer.validated_data.get('material_weight')
            if not re.fullmatch("^[0-9]*$",material_weight):
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "enter a valid material weight",
                    'result': [],
                    'additional_data': {},
                    }
                return Response(response_payload)
            serializer.save(user_id=id)
            pay_load=serializer.data
            response_payload = {    
                    'is_authenticated': True,
                    'status': status.HTTP_201_CREATED,
                    'messages':"Trip request generated successfully. Our team will contact you shortly. :)",
                    'result':[],
                    'additional_data': {}
                }
            return Response(response_payload)
        starting_date=serializer.data.get('starting_date')
        starting_point=serializer.data.get('starting_point')
        print(starting_point)
        destination=serializer.data.get('destination')
        print(destination)
        if not starting_point:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please provide the starting point",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not destination:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please provide the destination",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "not a valid constraint",
                'result': '',
                'additional_data': {},
            }
        return Response(response_payload)
#------------------------------------------------------------
class CreateeQueteView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        ambient_light=request.data.get('ambient_light')
        humidity=request.data.get('humidity')
        pitch_angle=request.data.get('pitch_angle')
        roll_angle=request.data.get('roll_angle')
        temprature=request.data.get('temprature')
        tilt=request.data.get('tilt')
        material_subtype=request.data.get('material_subtype')
        material_type=request.data.get('material_type')
        other_constraints=request.data.get('other_constraints')
        truck_type=request.data.get('truck_type')
        starting_date=request.data.get('starting_date')
        starting_time=request.data.get('starting_time')
        starting_point=request.data.get('starting_point')
        destination=request.data.get('destination')
        material_weight=request.data.get('material_weight')
        
        id=request.user.id
        print('ambient_light',ambient_light)
        print('humidity',humidity)
        print('pitch_angle',pitch_angle)
        print('roll_angle',roll_angle)
        print('temprature',temprature)
        print('tilt',tilt)
        print('material_subtype',material_subtype)
        print('material_type',material_type)
        print('other_constraints',other_constraints)
        print('truck_type',truck_type)
        print('starting_date',starting_date)
        print('starting_time',starting_time)
        print('starting_point',starting_point)
        print('destination',destination)
        print('material_weight',material_weight)
        if not starting_point:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "please provide the starting point",
                'result': [],
                'additional_data': {},
                }
            return Response(response_payload)
        if not starting_time:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "please enter the starting time of trip",
                'result': [],
                'additional_data': {},
                }
            return Response(response_payload)
        if not destination:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': "please provide the destination",
                    'result': [],
                    'additional_data': {},
                    }
            return Response(response_payload)
        if not starting_date:
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "please enter a valid starting_date",
                'result': [],
                'additional_data': {},
                }
            return Response(response_payload)
        
        if not re.match("^(0[1-9]|[12][0-9]|3[01])[-\\/](0[1-9]|1[012])[-\\/](19|20)\d\d$",starting_date):
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "please enter a valid starting date",
                'result': [],
                'additional_data': {},
                }
            return Response(response_payload)
        if not truck_type:
            response_payload={
                'is_authenticated':False,
                "status":status.HTTP_400_BAD_REQUEST,
                "messages":"please provide valid truck_type",
                "result":[],
                "additional_data":[]
            }

            return Response(response_payload)
        
        if not re.fullmatch("^[0-9]*$",material_weight):
            response_payload = {
                'is_authenticated': False,
                'status':status.HTTP_400_BAD_REQUEST,
                'messages': "enter a valid material weight",
                'result': [],
                'additional_data': {},
                }
            return Response(response_payload)
        material_instance=Material()
        material_instance.material_type=material_type
        material_instance.save()
        subtype_instance = MaterialSubtype()
        subtype_instance.material=material_instance
        subtype_instance.material_weight=material_weight
        subtype_instance.material_subtype=material_subtype
        subtype_instance.material_type=material_type
        subtype_instance.save()
        trip_instance=Trip.objects.create(submaterial=subtype_instance,material=material_instance,user_id=id,trip_status='requested',starting_point=starting_point,\
            destination=destination,truck_type=truck_type,starting_date=starting_date,other_constraints=other_constraints,starting_time=starting_time
                                          
                                          
                                          
                                          )
        trip_instance.save()
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "trip created success full",
                'result': [],
                'additional_data': {},
                }
        return Response(response_payload)
        
        
#-----------------------------------------------------------------
class TripRequestView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def list(self,request):
        id=request.user.id
        print('id',id)
        trip_status=request.GET.get('trip_status')
        if trip_status=='requested':
            queryset = Trip.objects.filter(user_id=id,trip_status='accepted')
            #print(queryset)
            pay_load1=[]
            for x in queryset:
                pay_load1.append({
                    'starting_date':x.starting_date,
                    'starting_time':x.starting_time,
                    'destination':x.destination,
                    'starting_point':x.starting_point,
                    'truck_type':x.truck_type,
                    'material_type':x.material.material_type,
                    'material_weight':x.submaterial.material_weight,
                    'submaterial':x.submaterial.material_subtype,
                    "created_at":post_meridiem_time(x.created_at),
                    'trip_status':x.trip_status,
                    'amount':x.amount,
                    "trip_id_show":x.trip_id_show,
                    'trip_id':x.id,
                    'truck_id':x.truck_id,
    
                    'constraints':{"temprature":x.submaterial.temprature,"humidity":x.submaterial.humidity,"tilt":x.submaterial.tilt,"ambient_light":x.submaterial.ambient_light,"pitch_angle":x.submaterial.pitch_angle,"roll_angle":x.submaterial.roll_angle}
                })
            queryset = Trip.objects.filter(user_id=id,trip_status='declined')
            pay_load2=[]
            for x in queryset:
                pay_load2.append({
                    'starting_date':x.starting_date,
                    'starting_time':x.starting_time,
                    'destination':x.destination,
                    'starting_point':x.starting_point,
                    'truck_type':x.truck_type,
                    'material_type':x.material.material_type,
                    'material_weight':x.submaterial.material_weight,
                    'submaterial':x.submaterial.material_subtype,
                    "created_at":post_meridiem_time(x.created_at),
                    'trip_status':x.trip_status,
                    'amount':x.amount,
                    'trip_id':x.id,
                    'truck_id':x.truck_id,
                    "trip_id_show":x.trip_id_show,
                    
                    'constraints':{"temprature":x.submaterial.temprature,"humidity":x.submaterial.humidity,"tilt":x.submaterial.tilt,"ambient_light":x.submaterial.ambient_light,"pitch_angle":x.submaterial.pitch_angle,"roll_angle":x.submaterial.roll_angle}
                })
            queryset = Trip.objects.filter(user_id=id,trip_status='requested')
            pay_load3=[]
            for x in queryset:
                pay_load3.append({
                    'starting_date':x.starting_date,
                    'starting_time':x.starting_time,
                    'destination':x.destination,
                    'starting_point':x.starting_point,
                    'truck_type':x.truck_type,
                    'material_type':x.material.material_type,
                    'material_weight':x.submaterial.material_weight,
                    'submaterial':x.submaterial.material_subtype,
                    "created_at":post_meridiem_time(x.created_at),
                    'trip_status':x.trip_status,
                    'amount':x.amount,
                    'trip_id':x.id,
                    'truck_id':x.truck_id,
                    "trip_id_show":x.trip_id_show,
                    'constraints':{"temprature":x.submaterial.temprature,"humidity":x.submaterial.humidity,"tilt":x.submaterial.tilt,"ambient_light":x.submaterial.ambient_light,"pitch_angle":x.submaterial.pitch_angle,"roll_angle":x.submaterial.roll_angle}
                })
            pay_load=pay_load1+pay_load2+pay_load3
            new_payload=(sorted(pay_load, key=lambda i: (i['starting_date'], i['starting_time'])))
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages':"data fetched succesfully",
                'result':new_payload[::-1],
                'additional_data': {}
            }
            return Response(response_payload)
        elif trip_status=='ongoing':
            print('id',id,'trip_status',trip_status)
            queryset = Trip.objects.filter(user_id=id,trip_status='ongoing',payment_status='paid')
            pay_load=[]
            for x in queryset:
                try:
                    truck = x.truck
                    try: 
                        driver = truck.driver
                        driver_name = driver.first_name
                    except AttributeError:
                            driver_name = None
                except Truck.DoesNotExist:
                    driver_name = None
                pay_load.append({
                    'starting_date':x.starting_date,
                    'starting_time':x.starting_time,
                    'destination':x.destination,
                    'starting_point':x.starting_point,
                    'trip_status':x.trip_status,
                    'starting_time':x.starting_time,
                    'driver':driver_name,
                    'helpline_number':x.helpiline_no,
                    'truck_id':x.truck_id,
                    'trip_id':x.id,
                    "trip_id_show":x.trip_id_show,
                    "created_at":post_meridiem_time(x.created_at),
                })
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
                'messages':"data fetched succesfully",
                'result':pay_load,
                'additional_data': {}
            }
            return Response(response_payload)
        elif trip_status=='upcoming':
            queryset = Trip.objects.filter(user_id=id,trip_status='upcoming',payment_status='paid').order_by('-starting_date', '-starting_time')
            pay_load=[]
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
                    "created_at":post_meridiem_time(x.created_at),
                    'trip_status':x.trip_status,
                    'amount':x.amount,
                    'trip_id':x.id,
                    'truck_id':x.truck_id,
                    "trip_id_show":x.trip_id_show,

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
            queryset=Trip.objects.filter(user_id=id,trip_status='completed',payment_status='paid').order_by('-driver_trip_complete_date')
            pay_load=[]
            for x in queryset:
                complete_date=x.driver_trip_complete_date
                if complete_date:
                    trip_end_date=complete_date.strftime('%Y-%m-%d,%H:%M:%S')
                    print(trip_end_date)
                else:
                    trip_end_date= None
                pay_load.append({
                    'destination':x.destination,
                    'starting_point':x.starting_point,
                    'truck_type':x.truck_type,
                    'starting_time':x.starting_time,
                    'start_date':x.starting_date,
                    'material_type':x.material.material_type,
                    'material_weight':x.submaterial.material_weight,
                    'submaterial':x.submaterial.material_subtype,
                    "created_at":post_meridiem_time(x.created_at),
                    'trip_status':x.trip_status,
                    'amount':x.amount,
                    'truck_id':x.truck_id,
                    'trip_id':x.id,
                    "trip_id_show":x.trip_id_show,
                    'trip_complete_date':trip_end_date,

                })
            response_payload = {    
                'is_authenticated': True,
                'status': status.HTTP_201_CREATED,
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
                'result': [],
                'additional_data': {},
            }
            return Response(response_payload)
        

def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAARFAxsaE:APA91bE1tOqaucZT1rPqcuS8_grxQ_RdIBG0djCxJ9zYZ1Vq-doygfi6l9Ee9dkxXRwGLQbUBJTQwVLNYGOECcr8vqZgTLDkSpsvgBg4eYVSOnpRzFdIZTMRRjBmh8e39vY8TqmAlOio"
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",    
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())
    
class SendNotification(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        user = User.objects.filter(fcm_token__isnull=False).values('fcm_token')
        fcm_tokens = [item['fcm_token'] for item in user] 
        print(fcm_tokens)
        firebase_object=FirePushNotication.objects.filter(fire_type=1).last()
        send_notification(fcm_tokens, firebase_object.title , firebase_object.description)
        return JsonResponse({"messages":"notification sent"})

def payment(request):
    if request.method=='POST':
        name = request.POST.get('name')
        amount = 50000
        data=request.POST.get('amount')
        client = razorpay.Client(
            auth=("rzp_test_AXPZiNHmqbpsZi", "YLM7OKjBwQBcI32kwgiHMbgM"))
        payment = client.order.create(data=data)
    return render(request, 'index.html') 


@csrf_exempt
def success(request):
    return render(request, "success.html")
# class PaymentView(viewsets.ViewSet):
#     def create(self,request):
#         data=request.data.get('amount')
#         payment(data)
#         return JsonResponse({'msg':'payment success'})


class FeedbackView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        trip_id=request.data.get('trip_id')
        if not trip_id or not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",trip_id):
            response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    'messages': "Please provide the trip id",
                    'result': [],
                    'additional_data': {},
                }
            return Response(response_payload)
        feedback=request.data.get('feedback')
        print(feedback)
        rating=request.data.get('rating')
        print(rating)
        try: 
            if feedback:
                Trip.objects.filter(id=trip_id).update(feedback=feedback)
            if rating:
                Trip.objects.filter(id=trip_id).update(rating=rating)
            response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    'messages': "Your feedback submitted successfully",
                    'result': [],
                    'additional_data': {},
                }
            return Response(response_payload)
        except:
            response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'messages': 'Some issue occurred.',
                    'result':False,
                }
            return Response(response_payload)

        
class AllNotificationView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def list(self,request):
        notification=FirePushNotication.objects.filter(status=True)
        serializer=NotificationSerializer(notification,many=True)
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "notifications list fetched succesfully",
                'result': serializer.data,
                'additional_data': {},
            }
        return Response(response_payload)
    
class UpdateProfile(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def update(self,request):
        id=request.user.id
        
        first_name=request.data.get('first_name')
        
        last_name=request.data.get('last_name')
        
        mobile=request.data.get('mobile')
        
        email=request.data.get('email')
        image=request.data.get('image')
        # print(image)
        if first_name:
            User.objects.filter(id=id).update(first_name=first_name)
        if email:
            try:
                # if not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email):
                #     return JsonResponse({'messages':'email not valid'})
                User.objects.filter(id=id).update(email=email)
            except IntegrityError :
                response_payload = {
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'e-mail already exists.',
                }
                return Response(response_payload)


        if mobile:
            # if not re.match("^\\d{9,13}$",mobile):
            #     return JsonResponse({'messages':'mobile number is not valid'})
            User.objects.filter(id=id).update(mobile=mobile)
        if last_name:
            User.objects.filter(id=id).update(last_name=last_name)
        if image:
            profile=Profile.objects.get(user_id=id)
            print(profile)
            profile.image=base64_file(image)
            profile.save()
            print("image saved successfully in db")
        user_obj=User.objects.filter(id=id)
        serializer=UpdateProfileSerializer(user_obj,many=True)
        print(serializer.data)
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "profile updated succesfully",
                'result': serializer.data,
                'additional_data': {},
            }
        return Response(response_payload)
    
    def list(self,request):
        id=request.user.id
        user_obj=User.objects.filter(id=id)
        #print(user_obj)
        serializer=UpdateProfileSerializer(user_obj,many=True)
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "Following are the user profile details.",
                'result': serializer.data,
                'additional_data': {},
            }
        return Response(response_payload)


class AcceptView(viewsets.ViewSet):
        permission_classes = (IsAuthenticated,)
        pagination_class = PageNumberPagination
        def create(self, request):
            id=request.user.id
            trip_id=request.data.get('trip_id')
            admin_id=request.data.get('admin_id')
            amount=request.data.get('amount')
            if not trip_id:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Please enter trip id',
                }
                return Response(response_payload)
            if not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",trip_id):
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Please enter a valid trip id',
                }
                return Response(response_payload)
            name = Trip.objects.values('id')
            if not amount:
                response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'messages': 'Please enter the amount',
            }
                return Response(response_payload)
            if not re.fullmatch("^[0-9]*$",amount):
                response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'messages': 'Please enter a valid amount',
            }
                return Response(response_payload)
            if not admin_id:
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Please enter the admin id',
                }
                return Response(response_payload)
            if not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",admin_id):
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Please enter a valid admin id',
                }
                return Response(response_payload)
            #print(name)
            for x in name:
                if str(trip_id) == str(x['id']):
                    print("yes")
                    try:
                        y=AdminResponse.objects.get(trip_id=trip_id,admin_id=admin_id)
                        y.customer_response='accept'
                        y.save()
                    except:
                        response_payload = {
                        'is_authenticated': False,
                        'status': status.HTTP_401_UNAUTHORIZED,
                        'messages': 'Trip ID or Admin ID not found',
                    }
                        return Response(response_payload)
                    try:
                        x=Trip.objects.get(id=trip_id, user_id=id)
                        x.trip_status='accepted'
                        x.amount=int(amount)
                        #x.truck_id=truck_id
                        x.admin_id=admin_id
                        x.save()   
                        response_payload = {
                                'is_authenticated': True,
                                'status': status.HTTP_200_OK,
                                'messages': 'Trip accepted'
                            }
                        return Response(response_payload)  
                    except:
                        response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'messages': 'Trip ID do not exist for this user ID',
            }
                        return Response(response_payload)

            response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'messages': 'Trip ID do not exist',
            }
            return Response(response_payload)
    

class ApplyCouponToSpecificCustomer(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        user_id = request.data.get('user_id')
        coupon_code = request.data.get('coupon_code')
        amount_paid = request.data.get('amount_paid')

        user = User.objects.get(id = user_id)
        try:
            coupons = Coupon.objects.get(coupon_code=coupon_code)
        except:
            response_payload = {
                        'is_authenticated': False,
                        'status': status.HTTP_400_BAD_REQUEST,
                        'messages': "Invalid Coupon",
                        'result': "",
                        'additional_data': {},
                    }
            return Response(response_payload)
            

        if user.coupon_code == coupon_code:
            new_amount = int(amount_paid) - coupons.coupon_amt
            user.coupon_code = None
            coupons.user_id = None
            user.save()
            response_payload = {
                        'is_authenticated': True,
                        'status': status.HTTP_200_OK,
                        'messages': "Coupon Applied",
                        'result': f"{coupon_code} Coupon Applied, New Amount : {new_amount}",
                        'additional_data': {},
                    }
            return Response(response_payload)
        
        else:
            response_payload = {
                        'is_authenticated': True,
                        'status': status.HTTP_200_OK,
                        'messages': "This user does not have any coupon or coupon expired",
                        'result': "",
                        'additional_data': {},
                    }
        return Response(response_payload)
    

class Orderid_generate(viewsets.ViewSet):
        permission_classes = (IsAuthenticated,)
        pagination_class = PageNumberPagination
        def create(self, request):
            amount=request.data.get('amount')
            id=request.user.id
            print('id', id)
            trip_id=request.data.get('trip_id')
            amount_paid=request.data.get('amount_paid')
            gst_per=request.data.get('gst_per')
            gst=request.data.get('gst')
            coupon_code=request.data.get('coupon_code')
            if coupon_code:
                query=User.objects.filter(id=id)
                print('query=User.objects.filter(id=id)')
                for x in query:
                    if not x.coupon_code:
                        response_payload = {
                            'is_authenticated':False,
                            'status':status.HTTP_401_UNAUTHORIZED,
                            'messages': 'Please enter a valid coupon',
                        }
                        return Response(response_payload)
                    print(x.coupon_code)
                    lst=x.coupon_code.split(',')
                    print(lst)
                    if coupon_code in lst:
                        response_payload = {
                            'status':status.HTTP_401_UNAUTHORIZED,
                            'messages': 'Coupon already used for this user.',
                        }
                        return Response(response_payload)
                if not User.objects.filter(coupon_code=coupon_code, id=id).exists():
                    print("okk")
                    if Coupon.objects.filter(coupon_code=coupon_code).exists():
                        x=Coupon.objects.get(coupon_code=coupon_code)
                        print(x.id)
                        coupon_id=x.id
                        query=User.objects.get(id=id)
    
                        old_coupon_code=query.coupon_code
                        query.coupon_code=old_coupon_code+','+coupon_code
                        query.save()
                            
                    else:
                        response_payload = {
                            'status':status.HTTP_401_UNAUTHORIZED,
                            'messages': 'Valid coupon code not found',
                        }
                        return Response(response_payload)
                

            if not trip_id or not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",trip_id):
                response_payload = {
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Valid Trip ID not found',
                }
                return Response(response_payload)
            if not amount_paid or int(amount_paid)<100:
                response_payload = {
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Valid amount to be paid not found',
                }
                return Response(response_payload)
            if not amount or int(amount)<100:
                response_payload = {
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Valid amount not found',
                }
                return Response(response_payload)
            
            if not gst_per:
                response_payload = {
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Valid gst percent not found',
                }
                return Response(response_payload)

            if not gst:
                response_payload = {
                    'status':status.HTTP_401_UNAUTHORIZED,
                    'messages': 'Valid gst Amount not found',
                }
                return Response(response_payload)
            

            notes={'Reason':'Testing razorpay'}
            
            name = Trip.objects.values('id')
            print(name)
            for x in name:
                print(x['id'])
                if str(trip_id) == str(x['id']):
                    print("yes")
                    if Trip.objects.filter(id=trip_id, user_id=id).exists():
                        client = razorpay.Client(auth=("rzp_test_AyroicDEhCgzZd", "gxZBaxiZkF0AK3MEpKMqn3G1"))
                        payment = client.order.create({'amount':amount_paid, 'currency':'INR', 'notes':notes})
                        print(payment)
                        print("Order id created!!")
                        x=Trip.objects.get(id=trip_id, user_id=id)
                        x.amount=amount
                        #print(payment['id'])
                        x.razorpay_order_id=payment['id']
                        x.gst_percent=gst_per
                        x.amount_paid=(int(amount_paid))
                        x.gst = gst

                        if coupon_code:
                            x.coupon_id=coupon_id
                        x.save()   
                        response_payload = {
                        'is_authenticated': True,
                        'status':status.HTTP_200_OK,
                        'messages': "Order id generated successfully",
                        'result': payment,
                        'additional_data': {},
                    }
                        return Response(response_payload) 
                    else:
                         response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'messages': 'Trip ID for this user not exist.',
            }
                         return Response(response_payload)  

            response_payload = {
                'is_authenticated': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'messages': 'Trip ID do not exist',
            }
            return Response(response_payload)        


              
# @csrf_exempt
class Payment_Webhooks(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated,)
    # pagination_class = PageNumberPagination
    def create(self,request):
        if request.method == 'POST':
            # data=request.data.get('data')
            data = json.loads(request.body)
            event = data['event']
            print("received data: ", data)
            if event == 'payment.captured':
                # Handle successful payment
                razorpay_payment_id = data['payload']['payment']['entity']['id']
                order = Trip.objects.get(razorpay_payment_id=razorpay_payment_id)
                if order:
                    order.issue = "Razorpay Webhook Working"
                    order.save()
                    
                    return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_204_NO_CONTENT)      


class Payment_Verfication(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def create(self, request):
        razorpay_order_id=request.data.get('razorpay_order_id')
        razorpay_payment_id=request.data.get('razorpay_payment_id')
        razorpay_signature=request.data.get('razorpay_signature')
        trip_id=request.data.get('trip_id')
        id=request.user.id      
        if not trip_id or not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",trip_id):
            response_payload = {
                'status':status.HTTP_401_UNAUTHORIZED,
                'messages': 'Valid Trip ID not found',
            }
            return Response(response_payload)
        if Trip.objects.filter(user_id=id,id=trip_id).exists():
            try:
                client = razorpay.Client(auth=("rzp_test_AyroicDEhCgzZd", "gxZBaxiZkF0AK3MEpKMqn3G1"))
                razorpay_order = client.order.fetch(razorpay_order_id)
                print(razorpay_order['status'])
                
                ver=client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
                })
                queryset = Trip.objects.filter(user_id=id,id=trip_id)
                for x in queryset:
                    print("ok")
                    x.razorpay_payment_id=razorpay_payment_id
                    x.razorpay_signature=razorpay_signature
                    x.payment_status=razorpay_order['status']
                    x.trip_status='upcoming'
                    x.payment_date=datetime.now()
                    x.save()   
                response_payload = {
                        'is_authenticated': True,
                        'status':status.HTTP_200_OK,
                        'messages': "Payment Verification successful",
                        'result': ver,
                        #'Payment_status': razorpay_order['status'],
                    }
                return Response(response_payload)
            except Exception as e:   
                queryset = Trip.objects.filter(user_id=id,id=trip_id)
                status1=client.order.payments(razorpay_order_id)
                dict=status1['items'][-1]
                issue=dict['error_description']
                for x in queryset:
                    x.payment_status=razorpay_order['status']
                    x.payment_date=datetime.now()
                    x.payment_issue=issue
                    x.save()   
                response_payload = {
                    'is_authenticated': False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'result':False,
                    'messages': 'Payment Verification failed',
                    'result':False,
                    #'Payment_status': status1,
                }
                return Response(response_payload)
        else:
            response_payload = {
                'status':status.HTTP_401_UNAUTHORIZED,
                'messages': 'Trip ID not found',
            }
            return Response(response_payload)

    

class CouponListView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def get(self, request):
        coupons=Coupon.objects.all()
        #print(coupons)
        paginated_coupons = self.pagination_class().paginate_queryset(coupons, request)
        serializer = Coupon_Serializer(paginated_coupons,many=True)
        #print(serializer.data)
        response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': 'following coupons are available',
                'coupon_types': serializer.data,
            }
        return Response(response_payload)

class TrackerLivelocation(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    def get(self, request):
        id=request.user.id
        trip_id=request.GET.get('trip_id')
        print('id',id)
        print('trip_id',trip_id)
        if not re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",trip_id):
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Please enter a valid trip id',
                    }
            return Response(response_payload)
        try:
            trip_obj=Trip.objects.get(id=trip_id, trip_status='ongoing', user_id=id)
            print('trip_obj',trip_obj)
        except:
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Trip do not exist for this user or has not started yet.',
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
                    'status':status.HTTP_200_OK,
                    'messages': "Trip successfully finished.",
                    'result':trip_data,
                    'additional_data': {},
                    }
        return Response(response_payload)

            


class RaiseIssueView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        trip_id=request.data.get('trip_id')
        id=request.user.id
        print(id)
        issue=request.data.get('issue')
        if not issue:
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Pls enter your issue.',
                    }
            return Response(response_payload)
        if trip_id:
            result=Trip.objects.filter(id=trip_id).update(issue=issue)
            print(result)
            if result==1:
                response_payload = {
                        'is_authenticated': True,
                        'status':status.HTTP_200_OK,
                        'messages': "Your issue w.r.t trip has been reported successfully",
                        'result': issue
                    }
            else:
                response_payload = {
                            
                            'is_authenticated': False,
                            'status': status.HTTP_404_NOT_FOUND,
                            'messages': 'Trip do not exist for this user.',
                        }
                return Response(response_payload)
        result=User.objects.filter(id=id).update(issue=issue)
        print(result)
        if result==1:
            response_payload = {
                    'is_authenticated': True,
                    'status':status.HTTP_200_OK,
                    'messages': "Your issue has been reported successfully",
                    'result': issue
                }
            return Response(response_payload)
        
        

# class SendAlerts(viewsets.ViewSet):
#     permission_classes = (IsAuthenticated,)
#     def create(self,request):
#         id=request.user.id
#         user = User.objects.filter(id=id,fcm_token__isnull=False).values('fcm_token')
#         fcm_tokens = [item['fcm_token'] for item in user] 
#         print(fcm_tokens)
#         firebase_object=FirePushNotication.objects.filter(fire_type=1).last()
#         print(firebase_object.title)
#         send_notification(fcm_tokens, firebase_object.title , firebase_object.description)
#         return JsonResponse({"messages":"notification sent"})
    


# class SendAlerts(viewsets.ViewSet):
#     permission_classes = (IsAuthenticated,)
#     def create(self,request):
#         id=request.user.id
#         trip_id='e7ed22ea-69f4-4ca1-ae66-5a71ffcca9b5'#request.data.get('trip_id')
#         trip_status=''
#         while trip_status!='completed':
#             if Trip.objects.filter(user_id=id,trip_status='started', id=trip_id).exists():
#                 queryset=Trip.objects.filter(id=trip_id)
#                 for x in queryset:
#                     trip_status=x.trip_status
#                     print(x.submaterial.temprature)
#                     print(x.truck.tracker_id)
#             else:
#                 response_payload = {
                        
#                         'is_authenticated': False,
#                         'status': status.HTTP_404_NOT_FOUND,
#                         'messages': 'Trip has not started yet.',
#                     }
#                 return Response(response_payload)

#         user = User.objects.filter(id=id,fcm_token__isnull=False).values('fcm_token')
#         fcm_tokens = [item['fcm_token'] for item in user] 
#         print(fcm_tokens)
#         firebase_object=FirePushNotication.objects.filter(fire_type=1).last()
#         print(firebase_object.title)
#         #send_notification(fcm_tokens, firebase_object.title , firebase_object.description)
#         return JsonResponse({"messages":"notification sent"})
    

class Add_addressbook(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        #trip_id=request.data.get('trip_id')
        id=request.user.id
        print(id)
        address=request.data.get('address')
        city=request.data.get('city')
        state=request.data.get('state')
        country=request.data.get('country')
        pincode=request.data.get('pincode')
        if address:
            result=User.objects.filter(id=id).update(address=address)
        if city:
            result=User.objects.filter(id=id).update(city=city)
        if state:
            result=User.objects.filter(id=id).update(state=state)
        if pincode:
            result=User.objects.filter(id=id).update(zipcode=pincode)
        if country:
            result=User.objects.filter(id=id).update(country=country)
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "Address book updated successfully.",
                'result': ''
            }
        return Response(response_payload)
    

    def list(self,request):
        id=request.user.id
        user_obj=User.objects.filter(id=id)
        #print(user_obj)
        serializer=ViewaddressbookSerializer(user_obj,many=True)
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "Following are the user address details.",
                'result': serializer.data[0],
                'additional_data': {},
            }
        return Response(response_payload)
    

class Upload_Kyc(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self,request):
        #trip_id=request.data.get('trip_id')
        id=request.user.id
        kyc_number=request.data.get('kyc_number')
        kyc_file=request.data.get('kyc_file')
        # print(kyc_number)
        # print(kyc_file)
        # print(id)
        if not kyc_number or not kyc_file:
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'Kyc number and Kyc file is mandatory to upload.',
                    }
            return Response(response_payload)
        User.objects.filter(id=id).update(kyc_numer=kyc_number)
        print("got user id")
        user=User.objects.get(id=id)
        print('user')
        user.kyc_file=kyc_file
        user.save()
        print('user saved')
        user_obj=User.objects.filter(id=id)
        serializer=UpdateKYCSerializer(user_obj,many=True)
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "KYC details uploaded succesfully",
                'result': serializer.data,
                'additional_data': {},
            }
        return Response(response_payload)
    
    def list(self,request):
        id=request.user.id
        user_obj=User.objects.filter(id=id)
        print(user_obj)
        serializer=UpdateKYCSerializer(user_obj,many=True)
        response_payload = {
                'is_authenticated': True,
                'status':status.HTTP_200_OK,
                'messages': "Following are the KYC details.",
                'result': serializer.data,
                'additional_data': {},
            }
        return Response(response_payload)
    


class Payment_historyView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination 
    def get(self, request):
        id=request.user.id
        history_done=Trip.objects.filter(user_id=id, payment_status='paid')
        paginated_history_done = self.pagination_class().paginate_queryset(history_done, request)
        serializer_done = PaymentHistorySerializer(paginated_history_done,many=True)
        history_fail=Trip.objects.filter(user_id=id, payment_status='attempted')
        paginated_history_fail = self.pagination_class().paginate_queryset(history_fail, request)
        serializer_fail = PaymentHistorySerializer(paginated_history_fail,many=True)
        print(serializer_fail.data)
        response_payload = {
                'is_authenticated': True,
                'status': status.HTTP_200_OK,
                'messages': 'Below is the payment history details available',
                'Payment_history': serializer_done.data+serializer_fail.data,
            }
        return Response(response_payload)
        
    

class KYC_statusView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        id=request.user.id
        if User.objects.filter(id=id, kyc_verified=True).exists():
            response_payload = {
                    'is_authenticated': True,
                    'status': status.HTTP_200_OK,
                    'messages': 'KYC verified successfully!',
                    'kyc_status': True,
                }
            return Response(response_payload)
        else:
            response_payload = {
                        
                        'is_authenticated': False,
                        'status': status.HTTP_404_NOT_FOUND,
                        'messages': 'KYC verification unsuccessful!',
                        'kyc_status': False,
                    }
            return Response(response_payload)


class DownloadInvoice(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        db_start = time.time()
        order_id = request.data.get('razorpay_order_id')
        if order_id =="" or order_id==" ":
            response_payload = {
                            
                                "is_authenticated": True,
                                "status": 400,
                                "error_code": 101,
                                "messages": "Please enter Order Id",
                                }
            return Response(response_payload)

        
        print('order_id ', order_id)

        # if Trip.objects.filter(razorpay_order_id=order_id).exists():
        #     trip = Trip.objects.get(razorpay_order_id=order_id)
        #     print(trip)
        #     print(trip.razorpay_order_id)

        try:
            # trip = Trip.objects.get(razorpay_order_id=order_id)
            trip = Trip.objects.select_related('user','material','submaterial','admin','truck').get(razorpay_order_id=order_id)

            # print("order_db = Student.objects.get(name='veeru')")     #you can filter using order_id as well
        except Trip.DoesNotExist:
            trip = None
            # print("order_db = None")
            response_payload = {
                            
                                "is_authenticated": False,
                                "status": 400,
                                "error_code": 101,
                                "messages": "Your Enter Valid Order Id",
                                }
            return Response(response_payload)
        if trip:
            admin_id_from_trip = trip.admin_id
            admin_profile_obj = AdminProfile.objects.get(user_id=admin_id_from_trip)


            
            total_amount = trip.gst + trip.amount
            print(trip.user.first_name)
            print(trip.admin.company_name)
            print(trip.user.last_name)
            if trip.user.first_name and trip.user.last_name is not None:
                customer_name = str(trip.user.first_name)+' '+ str(trip.user.last_name)
            else:
                customer_name = str(trip.user.first_name)

            context = {
                'customer_name': customer_name,
                'customer_email': trip.user.email,
                'customer_mobile': trip.user.mobile,
                'customer_address': trip.user.address,
                'payment_date': trip.payment_date,
                'material': trip.material.material_type,
                'submaterial': trip.submaterial.material_subtype,
                'material_weight':trip.submaterial.material_weight,
                'amount_paid': trip.amount,
                'gst': trip.gst,
                'transaction_id':  trip.razorpay_order_id,       
                'starting_point': trip.starting_point,
                'destination': trip.destination,
                'admin_name': admin_profile_obj.company_name,
                'total_amount':total_amount,
                'admin_id':trip.admin.id,
                'Vehicle_Number': "-",
                'pickup_date':'pickup_date',
                'pickup_time':'pickup_time',
                'pp_contact_no': 'pp_contact_no',
                'dimension':'dimension',
                'rate':'rate',   
                'discount':'discount',
                'insurance':'insurance'
       }

            

            # Create a temporary file in memory to store the PDF content
            pdf_data = io.BytesIO()

            # Create a PDF document
            template_path = 'invoice_final.html'
            template = get_template(template_path)
            html = template.render(context)
            pisa.CreatePDF(html, dest=pdf_data)

            # Save the PDF to the database model
            pdf_file = ContentFile(pdf_data.getvalue())

            # pdf = GeneratedPDF(title="Generated PDF")
            # invoice_name = trip.user.first_name+'_invoice'
            trip.invoice.save('invoice.pdf', pdf_file)
            print(trip.invoice.url)
            trip.save()

            # Close the temporary PDF file
            pdf_data.close()
            db_time = time.time() - db_start
            response= {
                "is_authenticated": True,
                "status": status.HTTP_200_OK,
                "messages": "Invoice Fetched Succesfully",
                'fileurl': trip.invoice.url
            }
            print('db_time ', db_time)
            return Response(response)
            
                # Create a bytestream buffer
                
                # buf = io.BytesIO()

                # # create a Canvas
                # c = canvas.Canvas(buf, pagesize=letter, bottomup=0) # letter size regular paper, A4 sheet

                # # create a textobject, that will tell us what to put on canvas
                # textob = c.beginText()
                # textob.setTextOrigin(inch, inch) # Measurement
                # textob.setFont('Helvetica', 14)  # text font and style

                # # add some lines of text
                # # lines = [
                # #          'this is line',
                # #          'this is line 2',
                # #          'this is line 3'
                # #          ]

                # lines = [str(trip.razorpay_order_id),str(trip.amount), trip.user.email, trip.user.first_name, str(trip.user.mobile)]
                

                # # loop throigh all lines
                # for line in lines:
                #     textob.textLine(line)

                # # finish up
                # c.drawText(textob)
                # c.showPage()
                # c.save()
                # buf.seek(0)
    
            # buf.close()
            # returning file as a response to the rondend for download
            

            # returning file as a response to the rondend for download
            # return FileResponse(buf, as_attachment=True, filename='invoice.pdf')
        else:
            response_payload = {
                            
                                "is_authenticated": False,
                                "status": 400,
                                "error_code": 101,
                                "messages": "Please Enter Valid Order Id",
                                }
            return Response(response_payload)

class CustomerCoupon(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):

        # user_id = request.user.id
        user_id = request.data.get('id')
        user = User.objects.get(id=user_id)
        coupons = Coupon.objects.get(coupon_code=user.coupon_code)
        coupon_paylod ={
            "coupon_code":  user.coupon_code,
            "coupon_amount": coupons.coupon_amt
        }
        print(user)
        response_payload = {
                        'is_authenticated': True,
                        'status': status.HTTP_200_OK,
                        'messages': "Coupons available for this customer",
                        'result': coupon_paylod,
                        'additional_data': {},
                    }
        return Response(response_payload)




class ApplyCouponToSpecificCustomer(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        user_id = request.user.id
        coupon_code = request.data.get('coupon_code')
        amount_paid = request.data.get('amount_paid')

        user = User.objects.get(id = user_id)
        try:
            coupons = Coupon.objects.get(coupon_code=coupon_code)
        except:
            response_payload = {
                        'is_authenticated': False,
                        'status': status.HTTP_400_BAD_REQUEST,
                        'messages': "Invalid Coupon",
                        'result': "",
                        'additional_data': {},
                    }
            return Response(response_payload)
            

        if user.coupon_code == coupon_code:
            new_amount = int(amount_paid) - coupons.coupon_amt
            user.coupon_code = None
            coupons.user_id = None
            user.save()
            payload = {
                "Coupon Code": coupon_code,
                "Old Amount" : amount_paid,
                "New Amount" : new_amount
            }
            response_payload = {
                        'is_authenticated': True,
                        'status': status.HTTP_200_OK,
                        'messages': "Coupon Applied",
                        'result': payload,
                        'additional_data': {},
                    }
            return Response(response_payload)
        
        else:
            response_payload = {
                        'is_authenticated': True,
                        'status': status.HTTP_200_OK,
                        'messages': "This user does not have any coupon or coupon expired",
                        'result': "",
                        'additional_data': {},
                    }
        return Response(response_payload)
class DeclineAdminResponseView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)
    def create(self,request):
        trip_id=request.data.get('trip_id')
        admin_id=request.data.get('admin_id')
        if not trip_id:
            response_payload = {
                        'is_authenticated': False,
                        'status': status.HTTP_400_BAD_REQUEST,
                        'messages': "Please specify the trip id",
                        'result': "",
                        'additional_data': {},
                    }
            return Response(response_payload)
        if not admin_id:
            response_payload = {
                        'is_authenticated': False,
                        'status': status.HTTP_400_BAD_REQUEST,
                        'messages': "Please specify the admin id",
                        'result': "",
                        'additional_data': {},
                    }
            return Response(response_payload)
        if AdminResponse.objects.filter(trip_id=trip_id,admin_id=admin_id).exists():
            AdminResponse.objects.filter(trip_id=trip_id,admin_id=admin_id).update(customer_response='declined')
            response_payload = {
                        'is_authenticated': True,
                        'status': status.HTTP_200_OK,
                        'messages': "Trip declined succesfully",
                        'result': "",
                        'additional_data': {},
                    }
            return Response(response_payload)
        else:
            response_payload = {
                        'is_authenticated': False,
                        'status': status.HTTP_400_BAD_REQUEST,
                        'messages': "Admin id or Trip does not exists",
                        'result': "",
                        'additional_data': {},
                    }
            return Response(response_payload)