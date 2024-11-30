from django.urls import path, include
# from harmonix_api.api.views import user_lists, user_details
from harmonix_api.api.views import *

urlpatterns = [
    path('register/', UserList.as_view(), name='user-list'),
    path('user/', UserList.as_view(), name='user-list'),
    path('user/detail/<int:pk>/', UserDetailsView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='user-login'),
    
    path('address/', AddressListView.as_view(), name='address'),
    path('user/update-address/<int:pk>/', UpdateAddressView.as_view(), name='user-details-update-address' ),
    path('address/detail/<str:pk>/', AddressDetail.as_view(), name='address-detail'),
    
    path('location/', LocationListView.as_view(), name='location'),
    path('location/detail/<int:pk>/', LocationDetailView.as_view(), name='location-details'),
    
    path('task/', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskUpdateView.as_view(), name='task-retrieve-update-delete'),
    path('user-task/', UserTaskListView.as_view(), name='user-task-list'),
    
    path('service/', TypeServiceView.as_view(), name='services'),
    
    path('create-service/', ServicesCreateView.as_view(), name='Create-Services'),
    path('list-service/', ServicesListView.as_view(), name='List-Services'),
    path('user/update-service/<int:pk>/', ServicesRetrieveUpdateView.as_view(), name='Update-Services'),
    path('user/service/<int:pk>/', ServicesRetrieveView.as_view(), name='Details-Services'),
    path('details-service/<int:pk>/', ServicesRetrieveDetailsView.as_view(), name='Details-Services'),
    
    path('portfolio/', UserPortfolioListCreateView.as_view(), name='List_Portfolio'),
    path('portfolio/<int:pk>', UserPortfolioRetrieveDestroyView.as_view(), name='List_Portfolio'),

    path('request/', RequestView.as_view(), name='Request'),
    path('request/<int:pk>/', GetRequestView.as_view(), name='Request-Detail'),
    path('request-status/<int:pk>/', PatchRequestStatusView.as_view(), name='Patch-Request-Detail'),
    
    path('booking/', BookingView.as_view(), name='Booking'),
    path('my-booking/', MyBookingStatus.as_view(), name='My-booking'),  
    path('booking/<int:pk>/', BookingUserView.as_view()),
    path('booking/<int:pk>/detail/', AcceptBookingView.as_view(), name='Booking-Detail'),
    path('rate-booking/<int:pk>/', RateBookingView.as_view(), name='Rate Booking'),
    path('rating/', RatingView.as_view(), name='Rating'),
    path('rating/<int:pk>/services/', RatingOfService.as_view(), name='RatingOfService'),
    path('send-verification-code/', SendVerificationCodeView.as_view(), name='send-verification-code'),
    path('register-verification/', RegisterVerificationCodeView.as_view(), name='registration code'),
    path('verify-code/', VerifyCode.as_view(), name='verify-code'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    
    # path('requests/', RequestView.as_view(), name='RequestView'),
    # path('notifications/<int:pk>/', BookingNotification.as_view(), name='Request-Notification'),
    # path('request-notification/<int:pk>/', RequestNotification.as_view(), name='Request-Notification'),
]