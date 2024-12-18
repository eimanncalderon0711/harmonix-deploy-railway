from django.db import models
from django.utils import timezone
import random
import string

# Create your models here.

class Address(models.Model):
    address_name = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.address_name

class User(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.fullname
    
class CharacterReference(models.Model):
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return f'Phone: {self.phone}'

class Certificate(models.Model):
    certificate = models.ImageField(upload_to='certificate_pics/')
    
    def __str__(self):
        return f'Certificate #{self.id}'
    
class AccountVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('decline', 'Declined'),
        ('accepted', 'Accepted'),   
    ]
    character_references = models.ManyToManyField(CharacterReference, related_name='AccountVerifications', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    certificate = models.ManyToManyField(Certificate, related_name='AccountVerifications', blank=True)
    valid_id = models.ImageField(upload_to='credential_pics/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    
    def __str__(self):
        return f'{self.user.fullname} - {self.status}'
    
class Location(models.Model):
    location_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.location_name

class TypeOfService(models.Model):
    service_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.service_name
   
class Services(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    TypeOfService = models.ManyToManyField(TypeOfService, related_name="services")

    def __str__(self):
        return f'service of {self.user.fullname}'
    
class Portfolio(models.Model):
    image = models.ImageField(upload_to='portfolio_pics/', null=True, blank=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='portfolios')
    
    def __str__(self):
        return f'Portfolio of {self.service.user.fullname}'

class Task(models.Model):
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="tasks")
    TypeOfService = models.ManyToManyField(TypeOfService, related_name="tasks")
    
    def __str__(self):
        return self.description

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('decline', 'Declined'),
        ('accepted', 'Accepted'),   
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='request')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests", db_index=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, db_index=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('inprogress', 'Inprogress'),
        ('done', 'Done'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    
    request_time = models.DateTimeField(auto_now_add=True)
    
    # If schedule_time and schedule_date are meant to store different things, clarify their roles:
    schedule_time = models.DateTimeField(auto_now=False, null=True, blank=True)
    schedule_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    
    address = models.CharField(max_length=255, null=True, blank=True)  # Increased length for full address
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.fullname}"
    
    
class Rating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # Define ratings from 1 to 5
    
    qualityOfWork = models.IntegerField(choices=RATING_CHOICES, default=0)
    affordability = models.IntegerField(choices=RATING_CHOICES, default=0)
    punctuality = models.IntegerField(choices=RATING_CHOICES, default=0)
    professionalism = models.IntegerField(choices=RATING_CHOICES, default=0)
    comment = models.CharField(max_length=255, null=True, blank=True)  # Optional comment
    
    def __str__(self):
        return f"Rating for booking #{self.booking.id}"
    
    
class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def generate_code(cls, length=6):
        return ''.join(random.choices(string.digits, k=length))
    
    @classmethod
    def create_for_email(cls, email):
        code = cls.generate_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=2)  # 1 minutes expiration
        return cls.objects.create(email=email, code=code, expires_at=expires_at)






