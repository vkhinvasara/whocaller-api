from django.test import TestCase
from django.urls import reverse, resolve
from .views import RegisterView, LoginView, ContactCreateView, UserContactsView, SpamNumberView, SearchByNameView, SearchByPhoneNumberView, ContactDetailView, MarkAsSpamView

class URLTests(TestCase):
    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_create_contact_url(self):
        url = reverse('create_contact')
        self.assertEqual(resolve(url).func.view_class, ContactCreateView)

    def test_user_contacts_url(self):
        url = reverse('user_contacts')
        self.assertEqual(resolve(url).func.view_class, UserContactsView)

    def test_mark_contact_as_spam_url(self):
        url = reverse('mark_contact_as_spam', args=[1])
        self.assertEqual(resolve(url).func.view_class, MarkAsSpamView)

    def test_spam_numbers_url(self):
        url = reverse('get_spam_numbers')
        self.assertEqual(resolve(url).func.view_class, SpamNumberView)

    def test_search_by_name_url(self):
        url = reverse('search_by_name')
        self.assertEqual(resolve(url).func.view_class, SearchByNameView)

    def test_search_by_phone_url(self):
        url = reverse('search_by_phone')
        self.assertEqual(resolve(url).func.view_class, SearchByPhoneNumberView)

    def test_contact_details_url(self):
        url = reverse('contact_details', args=[1])
        self.assertEqual(resolve(url).func.view_class, ContactDetailView)
        

##############################################################################################################################################################################

#Tests for registering a new user and logging in an existing user
    
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.register_url = reverse('register')
		self.login_url = reverse('login')
		self.user_data = {
			"phone_number": "+919881151392",
			"password": "testpassword123",
			"email": "testuser@example.com",
			"first_name": "Test",
			"last_name": "User",
		}


	def test_1_register_new_user(self):
		response = self.client.post(self.register_url, self.user_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		
	def test_2_login_existing_user(self):
		self.client.post(self.register_url, self.user_data, format='json')
		response = self.client.post(self.login_url, self.user_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
  
##############################################################################################################################################################################
  
#Tests for creating a new contact and viewing all contacts of a user  
class ContactTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_contact_url = reverse('create_contact')
        self.user_contacts_url = reverse('user_contacts')
        self.user_data = {
            "phone_number": "+919881151392",
            "password": "testpassword123",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
        }
        self.test_user = get_user_model().objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.test_user)

        self.contact_data = {
            "name": "Test Contact",
            "phone_number": "+919876543210"
        }

    def test_create_contact(self):
        response = self.client.post(self.create_contact_url, self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_contacts(self):
        self.client.post(self.create_contact_url, self.contact_data, format='json')
        response = self.client.get(self.user_contacts_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.contact_data['name'])
        self.assertEqual(response.data[0]['phone_number'], self.contact_data['phone_number'])
    
    
    ##############################################################################################################################################################################
    #Tests for marking a contact as spam and viewing all spam numbers
    
class SpamContactTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_contact_url = reverse('create_contact')
        self.user_contacts_url = reverse('user_contacts')
        self.mark_contact_as_spam_url = lambda contact_id: reverse('mark_contact_as_spam', kwargs={'contact_id': contact_id})
        self.spam_numbers_url = reverse('get_spam_numbers')
        self.user_data = {
            "phone_number": "+919881151392",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com"
        }
        self.test_user = get_user_model().objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.test_user)

        self.contact_data = {
            "name": "Test Contact",
            "phone_number": "+919876543210"
        }

    def get_last_contact_id(self):
        response = self.client.get(self.user_contacts_url, format='json')
        return response.data[-1]['id']

    def test_mark_contact_as_spam(self):
        self.client.post(self.create_contact_url, self.contact_data, format='json')
        contact_id = self.get_last_contact_id()
        response = self.client.put(self.mark_contact_as_spam_url(contact_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_spam_contacts(self):
        self.client.post(self.create_contact_url, self.contact_data, format='json')
        contact_id = self.get_last_contact_id()
        self.client.put(self.mark_contact_as_spam_url(contact_id), format='json')
        response = self.client.get(self.spam_numbers_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)  # check that response.data is not empty
        
        
##############################################################################################################################################################################
#Tests for searching contacts by name and phone number

class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='123456777', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.contact_data = {'name': 'Test Contact', 'phone_number': '+1234567890'}
        self.create_contact_url = reverse('create_contact')
        self.search_by_name_url = reverse('search_by_name')
        self.search_by_phone_url = reverse('search_by_phone')

    def test_search_by_name(self):
        self.client.post(self.create_contact_url, self.contact_data, format='json')
        response = self.client.get(f"{self.search_by_name_url}?query=Test%20Contact", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Test Contact')

    def test_search_by_phone_number(self):
        self.client.post(self.create_contact_url, self.contact_data, format='json')
        response = self.client.get(f"{self.search_by_phone_url}?query=%2B1234567890", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['phone_number'], '+1234567890')
        
        
##############################################################################################################################################################################
#Tests for viewing contact details

class ContactDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='123455678', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.contact_data = {'name': 'Test Contact', 'phone_number': '+1234567890'}
        self.create_contact_url = reverse('create_contact')
        
    def get_last_contact_id(self):
        response = self.client.get(reverse('user_contacts'), format='json')
        return response.data[-1]['id']

    def test_contact_details(self):
        self.client.post(self.create_contact_url, self.contact_data, format='json')
        contact_id = self.get_last_contact_id()
        response = self.client.get(reverse('contact_details', kwargs={'contact_id': contact_id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['contact']['name'], 'Test Contact')
        self.assertEqual(response.data['contact']['phone_number'], '+1234567890')

 #################################################################################################################################################################################
                                                    #END OF THE TESTS