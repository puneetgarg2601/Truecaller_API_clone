from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


'''Phone number model contains all the phone numbers including the registered users phone number and their contacts phone number. It also contains those phone number which are marked as spam but are not registered ones or contact ones'''

class PhoneNumber(models.Model):
  number = models.CharField(max_length=10, primary_key=True)
  spam_count = models.IntegerField(default=0)



'''
Making a custom user manager for the custom user model 
'''
class UserManager(BaseUserManager):
  def create_user(self, phone_no, name, password, **other_fields):
    """
    Creates and saves a User with the given name, phone number and password and email optional.
    """
    if not phone_no:
        raise ValueError('Users must provide a Phone Number')
    if other_fields.get('email'):
      email=self.normalize_email(email)
      user = self.model( phone_no=phone_no, name=name,**other_fields)

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, phone_no, name, password, **other_fields):
    """
    Creates and saves a superuser with the given name, phone number and password and email optional.
    """
    user = self.create_user(
        password=password,
        name=name, 
        phone_no=phone_no,**other_fields
    )
    user.is_admin = True
    user.save(using=self._db)
    return user



'''
Creates the custom user model by modifying the existing user model provided by django to store the details of the registered users.
'''

class User(AbstractBaseUser):
  name = models.CharField(
    verbose_name='Name',
    max_length=50,
  )
      
  email = models.EmailField(
    verbose_name='Email',
    max_length=100,
    default=''
  )
  phone_no = models.OneToOneField(PhoneNumber, verbose_name="phone", max_length=10, unique=True, on_delete=models.PROTECT)
  
  is_admin = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'phone_no'
  REQUIRED_FIELDS= ['name']
  
  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    self.set_password(self.password)
    super(User, self).save(*args, **kwargs)

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      return True

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      return self.is_admin



'''
Contact Model contains the details of all the contacts that are imported from all the registered user contact list
'''

class Contact(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="contact_user")
  name = models.CharField(max_length=50, verbose_name='Name')
  phone_no = models.ForeignKey(PhoneNumber, on_delete=models.PROTECT, verbose_name="Number")
  