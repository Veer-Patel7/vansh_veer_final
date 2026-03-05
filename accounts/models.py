from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Username required")
        
        if not email:
            raise ValueError("Email required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    CUSTOMER = 'customer'
    HOTEL_ADMIN = 'hotel_admin'
    SUPER_ADMIN = 'super_admin'


    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (HOTEL_ADMIN, 'Hotel Admin'),
        (SUPER_ADMIN, 'Super Admin'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)
    
    
    profile_photo = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True
    )

    # OTP field
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_customer(self):
        return self.role == self.CUSTOMER

    @property
    def is_hotel_admin(self):
        return self.role == self.HOTEL_ADMIN

    @property
    def is_super_admin(self):
        return self.role == self.SUPER_ADMIN

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset token for {self.user.email}"