""" Django manage.py command to load data to db """
import csv
from django.core.management.base import BaseCommand
from api import models

class Command(BaseCommand):
    """ command """
    help = 'Loads initial data into db from csv'

    def handle(self, *args, **options):
        # Grab admin user
        admin = models.User.objects.get(username='admin')

        # Read in restaurants.
        with open('csvs/LazyGuys-Restaurants.csv', newline='') as csvfile:
            print(next(csvfile)) # skip csv headers
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                models.Business.objects.get_or_create(
                    name=row[0],
                    description=row[1],
                    address=f'{row[2]} {row[3]},{row[4]}',
                    phone=row[5],
                    created_by=admin
                )

        # Read in categories and menus.
        with open('csvs/LazyGuys-Categories.csv', newline='') as csvfile:
            print(next(csvfile)) # skip csv headers
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                business = models.Business.objects.get(name=row[1])
                category, _ = models.Category.objects.get_or_create(
                    name=row[0],
                    description=row[3],
                    order=row[5],
                    active=True,
                    business=business,
                    created_by=admin
                )

                # Create menu and add to categories
                menu, created_menu = models.Menu.objects.get_or_create(
                    name=row[2],
                    business=business,
                    created_by=admin
                )

                if created_menu:
                    menu.save()

                category.menus.add(menu.pk)

        # Read in menu items.
        with open('csvs/LazyGuys-MenuItems.csv', newline='') as csvfile:
            print(next(csvfile)) # skip csv headers
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                print(row[1], row[3])
                business = models.Business.objects.get(name=row[1])
                category = models.Category.objects.get(business=business, name=row[3])
                menu = models.Menu.objects.get(name=row[2], business=business)
                models.MenuItem.objects.get_or_create(
                    name=row[0],
                    description=row[4],
                    price=row[5],
                    menu=menu,
                    created_by=admin
                )
