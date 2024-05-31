from django.urls import path
from .views import RegisterView, LoginView, ContactCreateView, UserContactsView, SpamNumberView, SearchByNameView, SearchByPhoneNumberView, ContactDetailView, MarkAsSpamView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('contacts/create', ContactCreateView.as_view(), name='create_contact'),
    path('contacts/', UserContactsView.as_view(), name='user_contacts'),
    path('contact/<int:contact_id>/spam/', MarkAsSpamView.as_view(), name='mark_contact_as_spam'),
    path('spam_numbers/', SpamNumberView.as_view(), name='get_spam_numbers'),
    path('search/name/', SearchByNameView.as_view(), name='search_by_name'),
    path('search/phone/', SearchByPhoneNumberView.as_view(), name='search_by_phone'),
    path('contact/<int:contact_id>/', ContactDetailView.as_view(), name='contact_details'),
]