from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Q
from api import models
from jet.admin import CompactInline

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

class BaseScheduleExceptionInline(CompactInline):
    model = models.ScheduleException
    extra = 0

class BaseScheduleInline(CompactInline):
    model = models.Schedule
    fields = ('name', 'start_date', 'end_date', 'start_time', 'end_time', 'recurrence_pattern')
    extra = 0
    show_change_link = True



class CategoryInline(CompactInline):
  model = models.Category
  extra = 0
  show_change_link = True

class MenuInline(CompactInline):
  model = models.Menu
  extra = 0
  show_change_link = True

  def formfield_for_manytomany(self, db_field, request=None, **kwargs):
    field = super(MenuInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # limit categories to the ones
    if db_field.name == 'categories':
        if request._obj_ is not None:
            field.queryset = field.queryset.filter(Q(business__exact=request._obj_) | Q(business__exact=None))
        else:
            field.queryset = field.queryset.none()

    return field

class BusinessScheduleInline(BaseScheduleInline):
  exclude = ['menu']

class BusinessScheduleExceptionsInline(BaseScheduleExceptionInline):
  exclude = ['menu']

class BusinessAdmin(BaseModelAdminInline):
  inlines = [CategoryInline, MenuInline, BusinessScheduleInline]

  def get_form(self, request, obj=None, **kwargs):
    # just save obj reference for future processing in Inline
    request._obj_ = obj
    return super(BusinessAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(models.Business, BusinessAdmin)


class MenuItemInline(CompactInline):
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


class ScheduleAdmin(BaseModelAdmin):
  fields = ('name', 'start_date', 'end_date', 'start_time', 'end_time', 'recurrence_pattern', 'business', 'menu')

admin.site.register(models.Schedule, ScheduleAdmin)
