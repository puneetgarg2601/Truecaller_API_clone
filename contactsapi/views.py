import re
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import serializer, models
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import F



'''View for the User registration functionality. Requires name, password and phone number for the registration and credentials should be passed via POST. Validates for the correct phone number and password format
Password Format validation: Should be at least 8 characters and Password should contain one letter and one number
Phone number validation: Should be a valid phone number and belongs to India only
'''
class SignUpView(APIView):
  def post(self, request):
    phone_no = request.data.get('phone_no')
    if models.User.objects.filter(phone_no=phone_no).exists():
      return Response({'msg':'Phone no. already registered'})
    serializer_phone = serializer.PhoneNoSerializer(data = {'number': request.data.get('phone_no')})
    if serializer_phone.is_valid(raise_exception=True):
      serializer_phone.save()
      user_serializer = serializer.UserSerializer(data = request.data)
      if user_serializer.is_valid():
        user = user_serializer.save()
        token = Token.objects.create(user=user)
        return Response({"msg": "Success", "Token":token.key})
      else:
        phone_instance = models.PhoneNumber.objects.get(number=request.data.get('phone_no'))
        phone_instance.delete()
        return Response(user_serializer.errors)



'''View for the sign in functionality. Sign In requires phone_no and password to be passed via POST and check for the password format validation and signin phone number should be registered
Password Format validation: Should be at least 8 characters and Password should contain one letter and one number
Phone number validation: Should be a valid phone number and belongs to India only
'''
class SignInView(APIView):
  def post(self, request):
    is_authenticated = authenticate(phone_no=request.data.get('phone_no'), password=request.data.get('password'))
    if is_authenticated:
      user = models.User.objects.get(phone_no=request.data.get('phone_no'))
      token = Token.objects.get(user=user)
      return Response({"msg": "Signed in Successfully", "Token":token.key})

    return Response({"msg":"Enter correct Credentials. Phone number should be a valid number and password should contain at least 8 characters. Password should contain at least one number and one letter"})



'''View for the search functionality. Can allow search via name and phone number. For searching the user should pass the token along with request. The keyword "Token" is followed by token that is generated via signup and login.The name or number is provided via GET.
'''
class SearchByNameOrNumberView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    if request.data.get('name'):
      name = request.data.get('name')
      qs1 = models.Contact.objects.filter(name__istartswith = name)
      ids = qs1.values_list('id', flat=True)
      list1 = list(qs1.values(Name = F('name'), Phone_no = F("phone_no__number"), Spam_count = F("phone_no__spam_count")))  
      list2 = list(models.Contact.objects.filter(name__contains = name).exclude(id__in = ids).values(Name = F('name'), Phone_no = F("phone_no__number"), Spam_count = F("phone_no__spam_count")))
      list1.extend(list2)
      print(list1)
      return Response(list1)


    if request.data.get('phone_no'):
      if not re.match(r'^[6-9]\d{9}$', request.data.get('phone_no')):
        return Response({"msg":"Enter a valid phone number"})
      phone_instance = models.PhoneNumber.objects.get(number = request.data.get('phone_no'))
      if not phone_instance:
        return Response({'msg':"Details not found."})
      user_instance = models.User.objects.filter(phone_no = phone_instance)
      if user_instance:
        ser = serializer.UserSerializer(user_instance, many=True)
        return Response(ser.data)
      contact_instance = models.Contact.objects.filter(phone_no = phone_instance)
      ser = serializer.ContactSerializer(contact_instance, many=True)
      return Response(ser.data)
      


'''
View to mark the contacts as spam. Phone number should be passed via POST to mark the number as spam and also the user should pass the token along with request to use this functionality
'''
class SpamView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  def post(serf, request):
    phone_no = request.data.get('phone_no')
    request.data['spam_count'] = 1
    try:
      instance = models.PhoneNumber.objects.get(number=phone_no)
      spam_count = instance.spam_count+1
      request.data['spam_count'] = spam_count
      ser = serializer.PhoneNoSerializer(instance, data={"number": request.data.get('phone_no'), "spam_count": spam_count})
      if ser.is_valid(raise_exception=True):
        res = ser.save()
        ser = serializer.PhoneNoSerializer(res)
      return Response(ser.data)
    except Exception:
      ser = serializer.PhoneNoSerializer(data={"number": request.data.get('phone_no'), "spam_count":1})
      if ser.is_valid(raise_exception=True):
        res = ser.save()
        ser = serializer.PhoneNoSerializer(res)
        return Response(ser.data)



'''View to add the contacts. The user should pass the token along with the request to add the contact. The contact information should contain name and phone number via POST to add contact.
'''  
class ContactView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    if not re.match(r'^[6-9]\d{9}$', request.data.get('phone_no')):
      return Response({"msg":"Enter a valid phone number"})
    qs = models.Contact.objects.filter(user = request.user.id, phone_no=request.data.get('phone_no'))
    if qs:
      return Response({'msg':'This number is already saved'})
    phone = models.PhoneNumber.objects.filter(number = request.data.get('phone_no'))
      
    if not phone:
      serial = serializer.PhoneNoSerializer(data={'number':request.data.get('phone_no'), 'spam_count':0})
      if serial.is_valid(raise_exception=True):
        serial.save()
    data = {**request.data, "user": request.user.id}
    ser = serializer.ContactSerializer(data = data)
    if ser.is_valid(raise_exception=True):
      ser.save()
      data = {"name":ser.data.get('name'), "phone_no":ser.data.get('phone_no')}
      return Response(data)

    return Response({'msg':'Something went wrong'})



