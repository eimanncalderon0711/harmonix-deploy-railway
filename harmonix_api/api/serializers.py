from rest_framework import serializers
from rest_framework.response import Response
from harmonix_api.models import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    # profile_picture_url = serializers.SerializerMethodField()
    
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'email': {'required': False},
            'password': {'required': False},
            'fullname': {'required': False},
        }
    
    # def get_profile_picture_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.profile_image:
    #         return request.build_absolute_uri(obj.profile_image.url)
    #     return None
        
    def validate(self, data):
        if 'email' in data:
            email = data['email']
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({'message':'Email already exists'})
        return data
    
    def create(self, validated_data):
        if 'password' not in validated_data or not validated_data['password']:
            raise serializers.ValidationError({'message': 'password is required'})
        
        if 'email' not in validated_data or not validated_data['email']:
            raise serializers.ValidationError({'message': 'email is required'})
        
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Check if 'password' is in the updated data
        if 'password' in validated_data:
            # Hash the new password before updating the user
            validated_data['password'] = make_password(validated_data['password'])
        
        return super().update(instance, validated_data)
    
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data['email']
        password = data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'message': 'Email Invalid'})
        
        if not check_password(password, user.password):
            raise serializers.ValidationError({'message': 'Password Invalid'})
        
        data['user'] = user
        return data
    
    
    
class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        
class TypeOfServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TypeOfService
        fields = '__all__'
        
    
class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = "__all__"
        
class UserTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    TypeOfService = TypeOfServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = "__all__"
        
class UserPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'  # Make sure to include 'service'

    # def create(self, validated_data):
    #     service = validated_data.pop('service')  # Pop service ID from data
    #     portfolio = Portfolio.objects.create(service=service, **validated_data)
    #     return portfolio
       
class UserServiceSerializer(serializers.ModelSerializer):
    # Accepts IDs
    portfolios = UserPortfolioSerializer(read_only=True, many=True)
    class Meta:
        model = Services
        fields = ['id', 'title', 'user', 'TypeOfService', 'portfolios']
        
class UserServiceViewSerializer(serializers.ModelSerializer):
    # Accepts IDs
    user = UserSerializer(read_only=True)
    TypeOfService = TypeOfServiceSerializer(read_only=True, many=True)
    portfolios = UserPortfolioSerializer(read_only=True, many=True)
    class Meta:
        model = Services
        fields = '__all__'

    # def create(self, validated_data):
    #     portfolios_data = validated_data.pop('portfolios', [])
    #     types_data = validated_data.pop('TypeOfService')

    #     service = Services.objects.create(**validated_data)
    #     service.TypeOfService.set(types_data)  # Associate the types

    #     for portfolio_data in portfolios_data:
    #         Portfolio.objects.create(service=service, **portfolio_data)

    #     return service

class UserUpdateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"
       
       
        
class ServiceRatingSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField()
    overall_avg = serializers.SerializerMethodField()
    qualityOfWork_avg = serializers.SerializerMethodField()
    affordability_avg = serializers.SerializerMethodField()
    punctuality_avg = serializers.SerializerMethodField()
    professionalism_avg = serializers.SerializerMethodField()

    class Meta:
        model = Services
        fields = [
            'id',
            'user',
            'title',
            'created_at',
            'TypeOfService',
            'ratings',
            'overall_avg',
            'qualityOfWork_avg',
            'affordability_avg',
            'punctuality_avg',
            'professionalism_avg',
        ]

    def get_ratings(self, obj):
        # Get all ratings associated with bookings of this service
        bookings = Booking.objects.filter(service=obj)
        ratings = Rating.objects.filter(booking__in=bookings)
        return RatingUserDetailSerializer(ratings, many=True).data  # Assuming you already have a RatingSerializer

    def get_overall_avg(self, obj):
        ratings = self.get_all_ratings_for_service(obj)
        total_reviews = len(ratings)
        if total_reviews > 0:
            total = sum([
                rating.qualityOfWork + rating.affordability + rating.punctuality + rating.professionalism
                for rating in ratings
            ])
            return total / (total_reviews * 4)  # 4 fields to average
        return 0

    def get_qualityOfWork_avg(self, obj):
        ratings = self.get_all_ratings_for_service(obj)
        return self.calculate_average(ratings, 'qualityOfWork')

    def get_affordability_avg(self, obj):
        ratings = self.get_all_ratings_for_service(obj)
        return self.calculate_average(ratings, 'affordability')

    def get_punctuality_avg(self, obj):
        ratings = self.get_all_ratings_for_service(obj)
        return self.calculate_average(ratings, 'punctuality')

    def get_professionalism_avg(self, obj):
        ratings = self.get_all_ratings_for_service(obj)
        return self.calculate_average(ratings, 'professionalism')

    def calculate_average(self, ratings, field):
        total_reviews = len(ratings)
        if total_reviews > 0:
            total = sum([getattr(rating, field) for rating in ratings])
            return total / total_reviews
        return 0

    def get_all_ratings_for_service(self, obj):
        """
        Helper method to get all ratings related to the service.
        This method will get ratings for all bookings associated with this service.
        """
        bookings = Booking.objects.filter(service=obj)
        ratings = Rating.objects.filter(booking__in=bookings)
        return ratings

class BookingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        
class RequestUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    class Meta:
        model = Request
        fields = "__all__"
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        
class BookingUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    service = UserServiceSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        
    def validate(self, attrs):
        booking = attrs.get('booking')
        # Ensure that a user can only rate a movie once
        if Rating.objects.filter(booking=booking).exists():
            raise serializers.ValidationError("You have already rated this movie.")

        return attrs
class RatingUserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = Rating
        fields="__all__"

class GetAllRatingSerializer(serializers.ModelSerializer):
    booking = BookingUserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = "__all__"
        
class VerififiedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountVerification
        fields = "__all__"

class ReferenceCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterReference
        fields = "__all__"

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"

        
        
