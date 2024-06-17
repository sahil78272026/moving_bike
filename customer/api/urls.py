from django.urls import path
from moving_bike.customer.api.views import VendorlistView_new,KYC_statusView,Payment_historyView,Upload_Kyc,Add_addressbook,RaiseIssueView,CouponListView,Payment_Webhooks, Payment_Verfication,Orderid_generate,AcceptView,\
    VendorlistView,CreateOTPView,VerifyOTPView,OrganizationView,TruckTypeView,MaterailTypeView,GetQouteView,TripRequestView,SendNotification,\
    success,payment,FeedbackView,TrackIdWIthTrackerView,AllNotificationView,UpdateProfile, DownloadInvoice,CreateeQueteView,TrackerLivelocation, ApplyCouponToSpecificCustomer, CustomerCoupon,DeclineAdminResponseView


urlpatterns = [
    path('create-otp/',CreateOTPView.as_view({'post':"create"}),name='create-otp'),
    path('verify-otp/',VerifyOTPView.as_view({'post':"create"}),name='otp-verufy'),
    path('org_signup/',OrganizationView.as_view()),
    path('truck_type/',TruckTypeView.as_view()),
    path('truck-tracker/',TrackIdWIthTrackerView.as_view()),
    path('material_type/',MaterailTypeView.as_view()),
    path('getqoute/',CreateeQueteView.as_view({'post':"create"}),name='get_quote'),
    path('get_qoute/',GetQouteView.as_view({'post':"create"}),name='get_quote'),
    path('trip_req/',TripRequestView.as_view({"get":"list"})),
    path('send-notifications/',SendNotification.as_view({"post":"create"})),
    path('payment/success' , success , name='success'),
    path('payment/' , payment , name='payment'),
    # path('payment2/',PaymentView.as_view({"post":"create"})),
    path('feedback/',FeedbackView.as_view({"post":"create"})),
    path('notification_list/',AllNotificationView.as_view({"get":"list"})),
    path('vendor_list/',VendorlistView.as_view({"get":"list"})),
    path('update_profile/',UpdateProfile.as_view({"put":"update"})),
    path('accept_view/',AcceptView.as_view({'post':"create"})),
    path('orderid_generate/' , Orderid_generate.as_view({'post':"create"}) , name='orderid_generate'),
    path('payment_verf/',Payment_Verfication.as_view({'post':"create"})),
    path('payment_webhook/',Payment_Webhooks.as_view({'post':"create"}) , name='payment_webhook'),
    path('coupon_type/',CouponListView.as_view()),
    # path('tracker_liveloc/',Tracker_livelocation.as_view()),
    path('trackerliveloc/',TrackerLivelocation.as_view()),
    path('issue/',RaiseIssueView.as_view({"post":"create"})),
    path('view_profile/',UpdateProfile.as_view({"get":"list"})),
    #path('send_alerts/',SendAlerts.as_view({"post":"create"})),
    path('add_addressbook/',Add_addressbook.as_view({"post":"create"})),
    path('view_addressbook/',Add_addressbook.as_view({"get":"list"})),
    path('kyc_upload/',Upload_Kyc.as_view({"post":"create"})),
    path('view_kyc/',Upload_Kyc.as_view({"get":"list"})),
    path('payment_history/',Payment_historyView.as_view()),
    path('kyc_status/',KYC_statusView.as_view()),
    path('vendor_list_new/',VendorlistView_new.as_view({"get":"list"})),
    path('invoice/', DownloadInvoice.as_view()),
    path('apply_coupon/', ApplyCouponToSpecificCustomer.as_view()),
    path('customer_coupon/', CustomerCoupon.as_view()),
    path('decline_trip_resp/',DeclineAdminResponseView.as_view({'post':'create'}))
]
