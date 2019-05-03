""" Serializers for models """

from django.contrib.auth.models import User
from rest_framework import serializers
from api import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ User serializer """

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')



class MenuItemSmallSerializer(serializers.HyperlinkedModelSerializer):
    """ MenuItem serializer """

    class Meta:
        model = models.MenuItem
        fields = ('name', 'description', 'order','price', 'active')


class MenuSerializer(serializers.ModelSerializer):
    """ Menu serializer """

    items = MenuItemSmallSerializer(many=True, read_only=True)

    class Meta:
        model = models.Menu
        fields = ('id', 'name', 'description', 'order', 'business',
                  'items', 'available')


class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    """ Business serializer """

    menus = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = models.Business
        fields = ('id', 'name', 'description', 'email', 'url', 'address', 'phone', 'menus', 'available')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """ Category serializer """

    class Meta:
        model = models.Category
        fields = ('name', 'description', 'order', 'items')


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
