""" Models for lazyguys """

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from recurrence.fields import RecurrenceField

# Create your models here.

class User(AbstractUser):
    """ User Model """


class BaseModel(models.Model):
    """ Base model """
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        editable=False,
        related_name='%(app_label)s_%(class)s_modified',
        related_query_name='%(app_label)s_%(class)ss',
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        editable=False,
        related_name='%(app_label)s_%(class)s_created',
        related_query_name='%(app_label)s_%(class)ss'
    )
    readonly_fields = ('created_by', 'created_at',
                       'modified_at', 'modified_by')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Business(BaseModel):
    """ Business model """
    description = models.TextField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name_plural = 'businesses'


class Category(BaseModel):
    """ Category model """
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, blank=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='categories', blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        verbose_name_plural = 'categories'


class Menu(BaseModel):
    """ Menu model """
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, blank=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='menus')
    categories = models.ManyToManyField(
        Category, related_name='menus', blank=True)


class MenuItem(BaseModel):
    """ Menu Item model """
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, blank=True)
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='items')
    color = models.CharField(max_length=200, blank=True)
    width = models.CharField(max_length=200, blank=True)
    height = models.CharField(max_length=200, blank=True)
    weight = models.CharField(max_length=200, blank=True)
    condition = models.CharField(max_length=200, blank=True)
    model = models.CharField(max_length=200, blank=True)
    price = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True, blank=True)
    categories = models.ManyToManyField(
        Category, related_name='items', blank=True)


class MenuItemModification(BaseModel):
    """ Menu Item Modification model """
    description = models.TextField(blank=True)
    value = models.IntegerField(default=0)
    item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name='modifications')


class Schedule(BaseModel):
    """ Schedule model """
    name = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField(blank=True, null=True)
    all_day = models.BooleanField(default=False, blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False, blank=True)
    recurrence_pattern = RecurrenceField(blank=True, null=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='available', blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE,
                             related_name='available', blank=True, null=True)

    class Meta:
        ordering = []
