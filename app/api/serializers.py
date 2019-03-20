""" Serializers for models """

from django.contrib.auth.models import User
from rest_framework import serializers
from api import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ User serializer """

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    """ Business serializer """

    class Meta:
        model = models.Business
        fields = ('name', 'description', 'email', 'url', 'address', 'phone', 'menus', 'available')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """ Category serializer """

    class Meta:
        model = models.Category
        fields = ('name', 'description', 'order', 'items')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    """ Menu serializer """

    class Meta:
        model = models.Menu
        fields = ('name', 'description', 'order', 'business',
                  'items', 'available', 'unavailable')


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    """ MenuItem serializer """

    class Meta:
        model = models.MenuItem
        fields = ('name', 'description', 'order', 'menu', 'color', 'width', 'height',
                  'weight', 'condition', 'model', 'price', 'active', 'categories')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    """ Schedulew serializer """

    class Meta:
        model = models.Schedule
        fields = ('name', 'start_date', 'end_date', 'all_day',
                  'is_recurring', 'recurrence_pattern', 'business', 'menu')
