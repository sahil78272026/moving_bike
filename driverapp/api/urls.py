from django.urls import path
from driverapp.api.views import DriverappView
from driverapp.api.views import TripCompleteVerifyOTPView, CompleteTripOTPsendView,DriverfetchremarkView,DriverVerifyOTPView,DriverTripStartOTPView,DriverTripRequestView,LoginViewSet,DriverLoginView,PersonalInformationEditView,CallBackURL,CallBackURLDetailView,\
    TrackerCallBackURL,TrackerDeviceInformation,TrackerDeviceDetails,DriverLanguageView,DeviceAlertView,PersonalInformationImageView,GoogleTripTrackerLatLongView



urlpatterns = [
    path('driverapp/',DriverappView.as_view({'get':"list"}),name='driverapp'),
    path('driverlogin/',DriverLoginView.as_view({'post':"create"}),name='dlogin'),
    path('driver-login/',LoginViewSet.as_view({'post':"create"}),name='driver_login'),
    # path('driveradd/',DriverAddView.as_view({'post':"create"}),name='driver_login'),
    path('update-profile/', PersonalInformationEditView.as_view(), name='view_update_profile'),
    path('update-image/', PersonalInformationImageView.as_view(), name='update_image_profile'),
    # path('urlget/', URLGETAPI.as_view(), name='view_update_profile'),
    path('callback/', CallBackURL.as_view(), name='callback'),
    path('tracker_call_back/', TrackerCallBackURL.as_view({'post':"create","get":"list"}), name='trakcer_callback'),
    path('google_trip_lat_lon/', GoogleTripTrackerLatLongView.as_view({'post':"create","get":"list"}), name='trip_lat_long'),
    path(r'tracker_call_back/<slug:slug>/', CallBackURLDetailView.as_view(), name='callback_detail'),
    path('devicelist/', TrackerDeviceInformation.as_view({"get":"list"}), name='device information'),
    path('devicelist/<slug:slug>/', TrackerDeviceDetails.as_view(), name='callback_detail'),
    path('language_list/', DriverLanguageView.as_view(), name='language_list'),
    path('alert/', DeviceAlertView.as_view(), name='alert device'),
    # path('send_notication/', SendNotification.as_view({"post":"create"}), name='callback_detail'),
    path('trip_req/',DriverTripRequestView.as_view({"get":"list"})),
    path('trip_start_sendOTP/',DriverTripStartOTPView.as_view({'post':"create"})),
    path('trip_start_OTPverify/',DriverVerifyOTPView.as_view({'post':"create"})),
    path('fetchremark/', DriverfetchremarkView.as_view({'get':"list"}),name='driverapp'),
    path('tripCompleteOTPsend/',CompleteTripOTPsendView.as_view({'post':"create"})),
    path('tripCompleteOTPverify/',TripCompleteVerifyOTPView.as_view({'post':"create"})),
    
]
