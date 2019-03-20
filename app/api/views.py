""" Views.py """

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from api import models, serializers

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class BaseViewSet(viewsets.ModelViewSet):
    """
    Base API view. Saves user with resource on update and create
    """
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class BusinessViewSet(BaseViewSet):
    """
    API endpoint that allows businesses to be viewed or edited.
    """
    queryset = models.Business.objects.all().order_by('-name')
    serializer_class = serializers.BusinessSerializer


class CategoryViewSet(BaseViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class MenuViewSet(BaseViewSet):
    """
    API endpoint that allows menus to be viewed or edited.
    """
    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuSerializer


class MenuItemViewSet(BaseViewSet):
    """
    API endpoint that allows menu items to be viewed or edited.
    """
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer


class ScheduleViewSet(BaseViewSet):
    """
    API endpoint that allows menu items to be viewed or edited.
    """
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
