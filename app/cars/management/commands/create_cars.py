from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cars.models import Car, User
import random

class Command(BaseCommand):
    help = 'Creates 12 Car instances with sample data'

    def handle(self, *args, **options):
        # Assuming there's at least one User in the database
        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create a User first.'))
            return

        # Sample data for cars
        car_names = ['Toyota Camry', 'Honda Accord', 'Ford Mustang', 'Chevrolet Impala', 'Nissan Altima', 'Subaru Outback', 'Audi A4', 'BMW 3 Series', 'Mercedes-Benz C-Class', 'Volkswagen Golf', 'Hyundai Elantra', 'Kia Optima']
        car_years = list(range(2000, 2023)) # Assuming current year is 2022

        for i in range(12):
            # Randomly select a user and a car name
            user = random.choice(users)
            car_name = car_names[i]
            car_year = random.choice(car_years)

            # Create and save a new Car instance
            car = Car(name=car_name, year=car_year, owner=user)
            car.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created {car_name} ({car_year}) for user {user.username}'))
