from django.db import models
from django.conf import settings
from recurrence.fields import RecurrenceField

# Create your models here.

class BaseModel(models.Model):
  name = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
  modified_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.DO_NOTHING,
    editable=False,
    related_name='%(app_label)s_%(class)s_modified',
    related_query_name='%(app_label)s_%(class)ss',
    blank=True,
    null=True
  )
  created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.DO_NOTHING,
    editable=False,
    related_name='%(app_label)s_%(class)s_created',
    related_query_name='%(app_label)s_%(class)ss'
  )
  readonly_fields = ('created_by', 'created_at', 'modified_at', 'modified_by')

  class Meta:
    abstract = True
    ordering = ['name']

  def __str__(self):
    return self.name


class Business(BaseModel):
  description = models.TextField(blank=True)
  address = models.CharField(max_length=200, blank=True)
  email = models.CharField(max_length=200, blank=True)
  phone = models.CharField(max_length=200, blank=True)
  url = models.CharField(max_length=200, blank=True)

  class Meta(BaseModel.Meta):
    verbose_name_plural = 'businesses'


class Menu(BaseModel):
  description = models.TextField(blank=True)
  order = models.IntegerField(default=0, blank=True)
  business = models.ForeignKey(Business, on_delete=models.DO_NOTHING, related_name='menus')


class MenuItem(BaseModel):
  description = models.TextField(blank=True)
  order = models.IntegerField(default=0, blank=True)
  menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='items')
  color = models.CharField(max_length=200, blank=True)
  width = models.CharField(max_length=200, blank=True)
  height = models.CharField(max_length=200, blank=True)
  weight = models.CharField(max_length=200, blank=True)
  condition = models.CharField(max_length=200, blank=True)
  model = models.CharField(max_length=200, blank=True)
  price = models.CharField(max_length=200, blank=True)
  active = models.BooleanField(default=True, blank=True)
  categories = models.ManyToManyField('Category', related_name='items')


class MenuItemModification(BaseModel):
  description = models.TextField(blank=True)
  value = models.IntegerField(default=0)
  item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, related_name='modifications')


class Category(BaseModel):
  description = models.TextField(blank=True)
  order = models.IntegerField(default=0, blank=True)

  class Meta(BaseModel.Meta):
    verbose_name_plural = 'categories'


class Schedule(BaseModel):
  name = models.CharField(max_length=200, blank=True)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField(blank=True)
  all_day = models.BooleanField(default=False, blank=True)
  start_time = models.TimeField(blank=True, null=True)
  end_time = models.TimeField(blank=True, null=True)
  is_recurring = models.BooleanField(default=False, blank=True)
  recurrence_pattern = RecurrenceField(blank=True, null=True)
  business = models.ForeignKey(Business, on_delete=models.DO_NOTHING, related_name='available', blank=True, null=True)
  menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='available', blank=True)

  class Meta:
    ordering = []


class ScheduleException(BaseModel):
  name = None
  event = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING, related_name='exceptions')
  date = models.DateTimeField()
  business = models.ForeignKey(Business, on_delete=models.DO_NOTHING, related_name='unavailable', blank=True, null=True)
  menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='unavailable', blank=True, null=True)

  class Meta:
    ordering = []
  
