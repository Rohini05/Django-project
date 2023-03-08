from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')
        

        email = self.normalize_email(email)    
        user = self.model(email=email, **other_fields)

        user.set_password(password)
        # user.save(using=self._db)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
       
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

class admin_details(AbstractBaseUser):
    name        = models.CharField(max_length=50, blank=True, null=True)
    email       = models.EmailField(verbose_name="email", unique=True, max_length=80,blank=True, null=True)
    password        = models.CharField(max_length=200, blank=True, null=True)
    is_staff        =models.BooleanField(default=False)
    is_superuser        =models.BooleanField(default=False)
    is_active        =models.BooleanField(default=False)
    is_admin        =models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    

    objects = MyAccountManager()

    def __str__(self):
        return self.email


    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


# Create your models here.
class User_Application_Detail(models.Model):
    Gender_CHOICES = (('Male', 'Male'),('Female', 'Female'))
    Ownership_CHOICES = (('Joint', 'Joint'),('Individual', 'Individual'))
    Category_CHOICES = (('Residential', 'Residential'),('Commerical', 'Commerical'))

    reviewer                   = models.ForeignKey(admin_details, related_name="reviewer", on_delete=models.CASCADE,blank=True, null=True)

    applicant_name                  = models.CharField(max_length=50, blank=True, null=True)

    mail_id                         = models.EmailField(max_length=50, blank=True, null=True)

    gender                          = models.CharField(max_length=10, choices=Gender_CHOICES,blank=True, null=True)

    district                        = models.CharField(max_length=50, blank=True, null=True)

    state                           = models.CharField(max_length=50, blank=True, null=True)
  
    pincode                         = models.IntegerField(blank=True, null=True)
    
    ownership                       = models.CharField(max_length=50, blank=True, null=True, choices=Ownership_CHOICES)
    
    gov_id_type                     = models.CharField(max_length=50, blank=True, null=True)
    
    id_num                          = models.CharField(max_length=50, blank=True, null=True)

    category                        = models.CharField(max_length=50, blank=True, null=True, choices=Category_CHOICES)

    load_Apply_kv                   = models.IntegerField(blank=True, null=True)

    status                        = models.CharField(max_length=50, blank=True, null=True, default="Pending")
    date_of_application           = models.DateTimeField(auto_now=True)
    date_of_approved              = models.DateTimeField(blank=True, null=True)
    modified_date                 = models.DateTimeField(blank=True, null=True)

    reviewer_comments              = models.TextField(blank=True, null=True)

    