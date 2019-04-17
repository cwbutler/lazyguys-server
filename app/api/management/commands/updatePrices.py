""" Django manage.py command to load data to db """
import csv
from django.core.management.base import BaseCommand
from api import models

class Command(BaseCommand):
    """ command """
    help = 'Adds prices to initial data into db from csv'

    def handle(self, *args, **options):
        # Read in menu items.
        with open('csvs/LazyGuys-MenuItems.csv', newline='') as csvfile:
            print(next(csvfile)) # skip csv headers
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                print(row[0], row[1], row[3])
                business = models.Business.objects.get(name=row[1])
                category = models.Category.objects.get(business=business, name=row[3])
                menu = models.Menu.objects.get(name=row[2], business=business)
                item = models.MenuItem.objects.get(name=row[0], menu=menu, description=row[4])
                item.price = row[5]
                item.save()
                category.items.add(item.pk)
