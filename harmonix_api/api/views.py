from harmonix_api.models import User, Address, Task, Location, TypeOfService, VerificationCode
from rest_framework.decorators import api_view
from rest_framework import status
from harmonix_api.api.serializers import *
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from harmonix_api.utils import send_verification_email
from django.core.exceptions import ValidationError
import random

##Table for registration and storing of user data
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Table for login user data
class LoginView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # Get user from validated data
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Login successful',
            'data': user_data
        })

#CRUD for user details
class UserDetailsView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message':'User does not exist'})
    
    def get(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated successfully', 'data': serializer.data})
        return Response(serializer.errors)
    
    def delete(self, request, pk, format=None):
        user = User.objects.filter(pk=pk)
        user.delete()
        return Response({'message': 'Deleted successfully deleted'})


#to update a users address
class UpdateAddressView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

#to add or create a new address or get list of addresses
class AddressListView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

#to get/update/delete the specific address
class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    
#to create a new location and get list of locations
class LocationListView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
class LocationDetailView(generics.RetrieveDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
#to create a new task and get list of tasks
class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer    
    
#to get the list of task with nested users
class UserTaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = UserTaskSerializer   
 
#to get or create a list of services
class TypeServiceView(generics.ListCreateAPIView):
    queryset = TypeOfService.objects.all()
    serializer_class = TypeOfServiceSerializer
    
#to get the list or create of services
class ServicesCreateView(generics.CreateAPIView):
    queryset = Services.objects.all()
    serializer_class = UserServiceSerializer
    
#to retrieve and update specific services
class ServicesRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = UserUpdateServiceSerializer
    
class ServicesListView(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class = UserServiceViewSerializer

class ServicesRetrieveView(generics.ListAPIView):  # Change this to ListAPIView
    serializer_class = UserServiceViewSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_field)  # Get user ID from the URL
        return Services.objects.filter(user_id=user_id)  # Ensure using user_id
    
class ServicesRetrieveDetailsView(generics.RetrieveUpdateDestroyAPIView):  # Change this to ListAPIView
    queryset = Services.objects.all()
    serializer_class = UserServiceViewSerializer
        
#to add portfolio for services and list of images
class UserPortfolioListCreateView(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = UserPortfolioSerializer
#to remove images in portfolio
class UserPortfolioRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = UserPortfolioSerializer

class RequestView(generics.ListCreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
       
class GetRequestView(generics.ListCreateAPIView):
    serializer_class = RequestUserSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['pk']
        task = Task.objects.get(user=user_id)
        return Request.objects.filter(task=task)

class PatchRequestStatusView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
       
class MyBookingStatus(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingUserSerializer

class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
      
class BookingUserView(generics.ListCreateAPIView):
    serializer_class = BookingUserSerializer 
    
    def get_queryset(self):
        user_id = self.kwargs['pk']
        service = Services.objects.get(user=user_id)
        return Booking.objects.filter(service=service)  

class RateBookingView(generics. RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingUserSerializer

class AcceptBookingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
class RatingView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
class RatingOfService(generics.RetrieveAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceRatingSerializer
    lookup_field = 'pk'
        
class GetAllMyRating(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingUserDetailSerializer
    
    # def get_queryset(self):
    #     user_id = self.kwargs['pk']
    #     service = Services.objects.get(user=user_id)
    #     booking = Booking.objects.get(service=service)
    #     return Response({"data": booking})
    
# @api_view(['POST'])
# def send_verification_code(request):
#     """
#     Endpoint to send a verification code to the user's email.
#     This can be used for email verification or password reset.
#     """
#     email = request.data.get('email')
    
#     # Validate email format
#     if not email:
#         return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         # Check if the email exists in the database
#         user = User.objects.filter(email=email).first()
#         if not user:
#             return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
#         # Generate a verification code and store it in the database
#         verification_code = VerificationCode.create_for_email(email)
        
#         # Send verification code to the user
#         send_verification_email(email, verification_code.code)
        
#         return Response({"message": "Verification code sent successfully"}, status=status.HTTP_200_OK)
    
#     except ValidationError as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def verify_code(request):
#     """
#     Endpoint to verify the code that was sent to the user's email.
#     """
#     email = request.data.get('email')
#     code = request.data.get('code')
    
#     # Validate inputs
#     if not email or not code:
#         return Response({"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         # Check if the verification code exists
#         verification = VerificationCode.objects.filter(email=email, code=code).first()
        
#         if not verification:
#             return Response({"error": "Invalid verification code or email."}, status=status.HTTP_400_BAD_REQUEST)
        
#         if verification.is_expired():
#             return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Verification success
#         return Response({"message": "Verification successful"}, status=status.HTTP_200_OK)
    
#     except VerificationCode.DoesNotExist:
#         return Response({"error": "Code not found for this email"}, status=status.HTTP_404_NOT_FOUND)


class RegisterVerificationCodeView(APIView):
    """
    Endpoint to send a verification code to the user's email.
    This can be used for email verification or password reset.
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        # Validate email format
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if there's an existing verification code for this email
            existing_code = VerificationCode.objects.filter(email=email).first()

            if existing_code:
                # If the existing code is not expired, return a message that it's already been sent
                if existing_code.expires_at > timezone.now():
                    return Response({"message": "A verification code has already been sent to this email."}, status=status.HTTP_400_BAD_REQUEST)
                
                # If the existing code has expired, delete it and generate a new code
                existing_code.delete()

            # Generate a new verification code and store it in the database
            verification_code = VerificationCode.create_for_email(email)

            # Send the verification code to the user
            send_verification_email(email, verification_code.code)
            return Response({"message": "Verification code sent successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
class SendVerificationCodeView(APIView):
    """
    Endpoint to send a verification code to the user's email.
    This can be used for email verification or password reset.
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        # Validate email format
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Query the user by email
            user = User.objects.filter(email=email).first()

            if not user:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Check if there's an existing verification code for this email
            existing_code = VerificationCode.objects.filter(email=email).first()

            if existing_code:
                # If the existing code is not expired, return a message that it's already been sent
                if existing_code.expires_at > timezone.now():
                    return Response({"message": "A verification code has already been sent to this email."}, status=status.HTTP_400_BAD_REQUEST)
                
                # If the existing code has expired, delete it and generate a new code
                existing_code.delete()

            # Generate a new verification code and store it in the database
            verification_code = VerificationCode.create_for_email(email)

            # Send the verification code to the user
            send_verification_email(email, verification_code.code)

            return Response({"message": "Verification code sent successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)      
        
class ResetPassword(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        newPassword = request.data.get('password')

        # Check if both email and newPassword are provided
        if not email or not newPassword:
            return Response({'message': 'Both email and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the user by email
            account = User.objects.get(email=email)
            
            # Prepare the data to update (only updating password)
            updated_data = {
                'password': newPassword
            }
            # Use the UserSerializer to validate and update the user's password
            serializer = UserSerializer(account, data=updated_data, partial=True)  # partial=True allows us to only update the password
            
            if serializer.is_valid():
                serializer.save()  # This will handle hashing the password via the `update()` method of the serializer
                return Response({'message': 'Password changed successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            # Handle case where user with the given email does not exist
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
         
class VerifyCode(APIView):
    def post(self, request):
        # Your logic for verifying code
        email = request.data.get('email')
        code = request.data.get('code')
        user = User.objects.filter(email=email).first()

        if user:
            return Response({"error": "User with this email already exist."}, status=status.HTTP_404_NOT_FOUND)
        
    # Validate inputs
        if not email or not code:
            return Response({"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Check if the verification code exists
            verification = VerificationCode.objects.filter(email=email, code=code).first()
            
            if not verification:
                return Response({"error": "Invalid verification code or email."}, status=status.HTTP_400_BAD_REQUEST)
            
            if verification.is_expired():
                return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verification success
            return Response({"message": "Verification successful"}, status=status.HTTP_200_OK)
        
        except VerificationCode.DoesNotExist:
            return Response({"error": "Code not found for this email"}, status=status.HTTP_404_NOT_FOUND)
        
        
class VerifiedAccountViews(APIView):
    
    def post(self, request):
        user_id = request.data.get('user')
        verified_account = AccountVerification.objects.filter(user=user_id).first()

        if not verified_account:
            return Response({"error": "This user has no verification request."}, status=status.HTTP_404_NOT_FOUND)

        serializer = VerififiedAccountSerializer(verified_account)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetVerifiedAccountViews(generics.CreateAPIView):
    queryset = AccountVerification.objects.all()
    serializer_class = VerififiedAccountSerializer
    # def create(self, request, *args, **kwargs):
    #     # Extract certificates and valid_id from the request
    #     certificates_data = request.FILES.getlist('certificate[]')  # Multiple images
    #     valid_id = request.FILES.get('valid_id')  # Single image for valid ID

    #     # Step 1: Create AccountVerification instance
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     account_verification = serializer.save(valid_id=valid_id)

    #     # Step 2: Save and link Certificate images
    #     for certificate_image in certificates_data:
    #         certificate_instance = Certificate.objects.create(certificate=certificate_image)
    #         account_verification.certificate.add(certificate_instance)

    #     # Step 3: Return serialized data
    #     return Response(self.get_serializer(account_verification).data, status=status.HTTP_201_CREATED)

class DeleteVerification(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccountVerification.objects.all()
    serializer_class = VerififiedAccountSerializer

class ReferenceView(generics.CreateAPIView):
    queryset = CharacterReference.objects.all()
    serializer_class = ReferenceCharSerializer

class CertificateView(generics.CreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
