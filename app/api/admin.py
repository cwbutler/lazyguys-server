from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from api import models

AdminSite.index_title = ugettext_lazy('Lazyguys Admin')
AdminSite.site_header = ugettext_lazy('Lazyguys Admin')
AdminSite.site_title = ugettext_lazy('Lazyguys Admin')

class BaseModelAdmin(admin.ModelAdmin):
  def save_model(self, request, obj, form, change):
    if obj.id:
      obj.modified_by = request.user
    else:
      obj.created_by = request.user
    
    super().save_model(request, obj, form, change)


class BaseModelAdminInline(BaseModelAdmin):
  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)

    for obj in formset.deleted_objects:
      obj.delete()

    for instance in instances:
      if instance.id:
        instance.modified_by = request.user
      else:
        instance.created_by = request.user
      instance.save()

    formset.save_m2m()


# Register your models here.

class BaseScheduleExceptionInline(admin.StackedInline):
    model = models.ScheduleException
    extra = 0

class BaseScheduleInline(admin.StackedInline):
    model = models.Schedule
    extra = 0


class MenuInline(admin.StackedInline):
  model = models.Menu
  extra = 0

class BusinessScheduleInline(BaseScheduleInline):
  exclude = ['menu']

class BusinessScheduleExceptionsInline(BaseScheduleExceptionInline):
  exclude = ['menu']

class BusinessAdmin(BaseModelAdminInline):
  inlines = [MenuInline, BusinessScheduleInline, BusinessScheduleExceptionsInline]

admin.site.register(models.Business, BusinessAdmin)


class MenuItemInline(admin.StackedInline):
    model = models.MenuItem
    extra = 0

class MenuScheduleInline(BaseScheduleInline):
  exclude = ['business']

class MenuScheduleExceptionsInline(BaseScheduleExceptionInline):
  exclude = ['business']

class MenuAdmin(BaseModelAdminInline):
  inlines = [MenuItemInline, MenuScheduleInline, MenuScheduleExceptionsInline]

admin.site.register(models.Menu, MenuAdmin)

admin.site.register(models.Category, BaseModelAdmin)

admin.site.register(models.MenuItem, BaseModelAdmin)
