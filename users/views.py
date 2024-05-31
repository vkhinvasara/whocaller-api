from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth import login
from .models import Contact, SpamNumber
from .serializers import ContactSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

#Import the User model
User = get_user_model()

#Create the RegisterView and LoginView classes
class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        if not phone_number or not password:
            return Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(phone_number=phone_number, password=password)
        login(request, user)
        return Response({'message': 'User created and logged in successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        if not phone_number or not password:
            return Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)





#Create the ContactCreateView and UserContactsView classes        
class ContactCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user
        Contact.objects.create(**data)
        return Response({'message': 'Contact created successfully'}, status=status.HTTP_201_CREATED)
    
 
class MarkAsSpamView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, contact_id):
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        contact.spam = True
        contact.save()
        SpamNumber.objects.create(phone_number=contact.phone_number, name = contact.name)
        return Response({'message': 'Contact marked as spam and added to SpamNumber'}, status=status.HTTP_200_OK)
        
class UserContactsView(ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)
    
    
    
    
    
    
 #Create the SearchByNameView and SearchByPhoneNumberView classes   
class SearchByNameView(ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query')
        return Contact.search_by_name(query)

class SearchByPhoneNumberView(ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query')
        return Contact.search_by_phone_number(query)
    
class ContactDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contact_id):
        contact = Contact.objects.get(id=contact_id)
        if not contact:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'contact': ContactSerializer(contact).data}, status=status.HTTP_200_OK)

    
    
    
    
    
#Create the SpamNumberView class    
class SpamNumberView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        name = request.data.get('name')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        SpamNumber.objects.create(phone_number=phone_number, name = name)
        return Response({'message': 'Spam number added successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        spam_numbers = SpamNumber.objects.all()
        return Response({'spam_numbers': [{'phone_number': number.phone_number, 'name': number.name} for number in spam_numbers]}, status=status.HTTP_200_OK)
    
    
    