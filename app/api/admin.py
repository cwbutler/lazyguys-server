""" Admin classes """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy
from django.db.models import Q
from jet.admin import CompactInline
from api import models

admin.site.register(models.User, UserAdmin)

admin.AdminSite.index_title = ugettext_lazy('Lazyguys Admin')
admin.AdminSite.site_header = ugettext_lazy('Lazyguys Admin')
admin.AdminSite.site_title = ugettext_lazy('Lazyguys Admin')


class BaseModelAdmin(admin.ModelAdmin):
    """ Base admin class """
    search_fields = ['name']

    def get_form(self, request, obj=None, change=False, **kwargs):
        # save obj reference for future processing
        request._obj_ = obj
        return super(BaseModelAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.id:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user

        super(BaseModelAdmin, self).save_model(request, obj, form, change)

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


class BaseScheduleInline(CompactInline):
    """ Base Schedule inline class """
    model = models.Schedule
    fields = ('name', 'start_date', 'start_time',
              'end_time', 'recurrence_pattern')
    extra = 0
    show_change_link = True


class CategoryInline(CompactInline):
    """ Category inline class """
    model = models.Category
    extra = 0
    show_change_link = True


class MenuInline(CompactInline):
    """ Menu inline class """
    model = models.Menu
    extra = 0
    show_change_link = True

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(MenuInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

        # limit categories to the ones created by a business or globally
        if db_field.name == 'categories':
            if request._obj_ is not None:
                business = request._obj_ if isinstance(
                    request._obj_, models.Business) else request._obj_.business
                field.queryset = field.queryset.filter(
                    Q(business__exact=business) | Q(business__exact=None))
            else:
                field.queryset = field.queryset.none()

        return field


class BusinessScheduleInline(BaseScheduleInline):
    """ Business Schedule inline class """
    exclude = ['menu']


class BusinessAdmin(BaseModelAdmin):
    """ Business admin class """
    inlines = [CategoryInline, MenuInline, BusinessScheduleInline]


admin.site.register(models.Business, BusinessAdmin)


class MenuItemInline(CompactInline):
    """ MenuItem inline class """
    model = models.MenuItem
    extra = 0

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(MenuItemInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

        # limit categories to the ones created by a business or globally
        if db_field.name == 'categories':
            if request._obj_ is not None:
                business = request._obj_ if isinstance(
                    request._obj_, models.Business) else request._obj_.business
                field.queryset = field.queryset.filter(
                    Q(business__exact=business) | Q(business__exact=None))
            else:
                field.queryset = field.queryset.none()

        return field


class MenuScheduleInline(BaseScheduleInline):
    """ Menu Schedule inline class """
    exclude = ['business']


class MenuAdmin(BaseModelAdmin):
    """ Menu admin class """
    inlines = [MenuItemInline, MenuScheduleInline]
    list_display = ('business', 'name')
    search_fields = ['name', 'business__name']


admin.site.register(models.Menu, MenuAdmin)


class CategoryAdmin(BaseModelAdmin):
    """ Category admin class """
    list_display = ('business', 'name')
    search_fields = ['name', 'business__name']

admin.site.register(models.Category, CategoryAdmin)

class MenuItemAdmin(BaseModelAdmin):
    """ Menu item class """
    list_display = ('name', 'menu')
    search_fields = ['name', 'menu__name']

admin.site.register(models.MenuItem, MenuItemAdmin)


class ScheduleAdmin(BaseModelAdmin):
    """ Schedule admin class """
    fields = ('name', 'start_date', 'start_time', 'end_time',
              'recurrence_pattern', 'business', 'menu')


admin.site.register(models.Schedule, ScheduleAdmin)
