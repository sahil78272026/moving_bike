from django.urls import path
from superadmin.api.views import LoginViewSet,SuperAdminRegisterView,GetCustomerView,CustomerTripDetailsView,AdminListView,TrackerDeviceGeneric,\
    TrackerHistoryView,TrackerDeviceDetails,TrackerListInfoView,TrackerAssignView,TrackerListAssignView,SendOtpView,VerifyOtpView,ResetPasswordView,AdminStatusUpdate,AssignAdminTrip,DeactivateAdmin,\
    CreateCouponCodeAPIView, AssignCoupon, ListAllAvailableCouponsToApply, CustomerByNoOfOrders,AdminSubscriptionDetails, BulkAddTracker,AdminPaymentDetailsView,\
    AdminUpdateAPI
    


urlpatterns=[
    path('login/',LoginViewSet.as_view({'post':"create"}),name='superadmin-login'),
    path('signup/',SuperAdminRegisterView.as_view({'post':"create"}),name='superadmin-signup'),
    path('get_customer',GetCustomerView.as_view({'get':'list'})),
    path('customer_details/',CustomerTripDetailsView.as_view({'get':'list'})),
    path('admin_list/',AdminListView.as_view({'get':'list'})),
    path('device/',TrackerDeviceGeneric.as_view()),
    path('adminstatus/',AdminStatusUpdate.as_view()),
    path('deactivate_admin/',DeactivateAdmin.as_view()),
    path('update_admin/',AdminUpdateAPI.as_view({'put':'update'})),
    path('device/<slug:slug>/',TrackerDeviceDetails.as_view()),
    path('device/history/<slug:slug>/',TrackerHistoryView.as_view()),
    path('tracker_info_list/',TrackerListInfoView.as_view({'get':'list'})),
    path('tracker_assign/',TrackerAssignView.as_view({'post':'create'})),
    path('tracker_list/',TrackerListAssignView.as_view({'get':'list'})),
    path('send_otp/',SendOtpView.as_view({'post':'create'})),
    path('verify_otp/',VerifyOtpView.as_view({'post':'create'})),
    path('reset_password/',ResetPasswordView.as_view({'post':'create'})),
    path('assign_trip_admin/',AssignAdminTrip.as_view({'post':'create'})),
    path('create_coupon_code/',CreateCouponCodeAPIView.as_view()),
    path('assign_coupon/',AssignCoupon.as_view()),
    path('coupon_list/',ListAllAvailableCouponsToApply.as_view()),
    path('user_order_list/',CustomerByNoOfOrders.as_view()),
    path('admin_subscription/',AdminSubscriptionDetails.as_view({'get':'list'})),
    path('tracker_add_bulk/',BulkAddTracker.as_view()),
    path('payment_to_admin/',AdminPaymentDetailsView.as_view({'get':'list'}))

]