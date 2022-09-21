from rest_framework import serializers
from . import models
import re



'''
Serializer for the User model. Also validates the password entered by the users
'''
class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(style={"input_type":"password"}, write_only=True)
  class Meta:
    model = models.User
    fields = ['phone_no', 'name', 'password', 'email']

  def validate_password(self, data):
    password = data

    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
      raise serializers.ValidationError("Password should contain at least 8 characters.Password shoul contain at least one letter and one number.")
    return data



'''
Serializer for the signin functionality. Uses the user model to authenticate the user and also validates the phone_no
'''

class SignInSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.User
    fields = ['phone_no']

  def validate_phone_no(self, data):
    if not re.match(r'^[6-9]\d{9}$', data):
      raise serializers.ValidationError("Enter a valid phone number")
    return data


'''
Serializer for the Phone number model.
'''

class PhoneNoSerializer(serializers.ModelSerializer):

  class Meta:
    model = models.PhoneNumber
    fields = ['number', 'spam_count']

  def validate_number(self, data):
    if not re.match(r'^[6-9]\d{9}$', data):
      raise serializers.ValidationError("Enter a valid phone number")
    return data


'''
Serializer for the contacts model.
'''

class ContactSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Contact
    fields = '__all__'

  
  
