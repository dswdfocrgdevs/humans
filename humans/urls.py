from django.urls import path
from django.conf import settings
from humans.views import DashboardsView
from . import views


from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('rsp.urls')),
    # path('admin/', admin.site.urls),
    # path('humans/api/', include('api.urls')),  # Include the api urls
]
