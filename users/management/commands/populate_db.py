from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Contact, SpamNumber
import faker

class Command(BaseCommand):
    help = 'Populates the database.'

    def handle(self, *args, **options):
        fake = faker.Faker()

        User = get_user_model()

        for _ in range(100):
            user = User.objects.create_user(
                phone_number=fake.phone_number(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password = "password",
                email=fake.email(),
            )

            for _ in range(5):
                Contact.objects.create(
                    user=user,
                    name=fake.name(),
                    phone_number=fake.phone_number(),
                    email_address=fake.email(),
                    spam=fake.boolean(),
                )

            if fake.boolean():
                SpamNumber.objects.create(
                    phone_number=fake.phone_number(),
                    name = fake.name(),
                )

        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))
        
  
  
#For deleting the data from the database
       
# from django.contrib.auth import get_user_model
# from users.models import Contact, SpamNumber

# User = get_user_model()
# User.objects.all().delete()
# Contact.objects.all().delete()
# SpamNumber.objects.all().delete()