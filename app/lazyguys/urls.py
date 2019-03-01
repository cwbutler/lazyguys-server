"""lazyguys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from api import views
from rest_framework.documentation import include_docs_urls
from django.views.i18n import JavaScriptCatalog

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'business', views.BusinessViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'menu', views.MenuViewSet)
router.register(r'menuItem', views.MenuItemViewSet)
router.register(r'schedule', views.ScheduleViewSet)
router.register(r'scheduleException', views.ScheduleExceptionViewSet)

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),
    url(r'^', include('rest_framework.urls')), # REST api
    url(r'^docs/', include_docs_urls(title='LazyGuys API')),
    path('', include(router.urls)),
]

js_info_dict = {
    'packages': ('recurrence', ),
}

urlpatterns += [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
]
