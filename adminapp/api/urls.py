from django.urls import path
from adminapp.api.views import AdminResponseView, AdminappView,AdminRegisterView,SendOtpView,VerifyOtpView,ResetPasswordView,LoginViewSet,ALLDeviceAlertView, \
    FleetAddView,VehicleTruckView,AddDriverView,AdminAccountView,SupervisorView,AdminTripView,AssignTripView,AdminPaymentView,TrackerListView,Tracker_location,DriverListView,HelpDeskView,\
    TrackerHistoryAdminView,TrackerDeviceAdminDetails,AdminTrackerListView,AllDeviceLocationView,AdminAlertTripView,TruckCountView,LocationBasedTrackerView,\
        TrackerLocationView


urlpatterns = [
    path('adminapp/',AdminappView.as_view({'get':"list"}),name='adminapp'),
    path('signup/',AdminRegisterView.as_view({'post':"create"}),name='admin-signup'),
    path('login/',LoginViewSet.as_view({'post':"create"}),name='admin-login'),
    path('send_otp/',SendOtpView.as_view({'post':'create'})),
    path('verify_otp/',VerifyOtpView.as_view({'post':'create'})),
    path('reset_pass/',ResetPasswordView.as_view({'post':'create'})),
    path('device-alert/',ALLDeviceAlertView.as_view(),name='device-alert'),
    path('fleet_add/',FleetAddView.as_view({'post':'create','get':'list','put':'update','delete':'destroy'})),
    # path('fleet_add_update/',FleetUpdateCrudAPIView.as_view({'post':'create','get':'list','put':'update','delete':'destroy'})),
    path('vehicle/',VehicleTruckView.as_view(),name='vehicle-get'),
    path('add_driver/',AddDriverView.as_view({'post':'create','get':'list','put':'update','delete':'destroy'}),name='adddriver'),
    path('admin_account/',AdminAccountView.as_view({'post':'create','get':'list','put':'update','delete':'destroy'})),
    path('view_supervisor/',SupervisorView.as_view({'get':'list'})),
    path('admin_response/',AdminResponseView.as_view({'post':'create'})),
    path('admin_trip/',AdminTripView.as_view({'get':'list'})),
    path('assign_trip/',AssignTripView.as_view({'post':'create'})),
    path('payment_status/',AdminPaymentView.as_view({'get':'list'})),
    path('tracker_list/',TrackerListView.as_view({'get':'list'})),
    path('tracker_location/',Tracker_location.as_view({'get':'list'})),
    path('trackerlocation/',TrackerLocationView.as_view({'get':"list"})),
    path('driver_list/',DriverListView.as_view({'get':'list'})),
    path('device',TrackerDeviceAdminDetails.as_view()),
    path('device/history',TrackerHistoryAdminView.as_view()),
    path('help_desk_query/',HelpDeskView.as_view({'post':'create'})),
    path('admin_tracker_list/',AdminTrackerListView.as_view({'get':'list'})),
    path('all_device_location/',AllDeviceLocationView.as_view({'get':'list'})),
    path('alert/',AdminAlertTripView.as_view({"get":"list"}),name="admin-alert"),
    path('truck_count/',TruckCountView.as_view({'get':'list'})),
    path('location_details/',LocationBasedTrackerView.as_view({'get':'list'}))
]
