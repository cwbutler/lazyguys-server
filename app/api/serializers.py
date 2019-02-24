from django.contrib.auth.models import User
from api import models
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Business
        fields = ('name', 'description', 'email', 'url', 'address', 'phone', 'menus', 'available', 'unavailable')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'description', 'order', 'items')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Menu
        fields = ('name', 'description', 'order', 'business', 'items', 'available', 'unavailable')


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ('name', 'description', 'order', 'menu', 'color', 'width', 'height', 'weight', 'condition', 'model', 'price', 'active', 'categories')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Schedule
        fields = ('name', 'start_date', 'end_date', 'all_day', 'is_recurring', 'recurrence_pattern', 'business', 'menu')


class ScheduleExceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ScheduleException
        fields = ('event', 'date', 'business', 'menu')
