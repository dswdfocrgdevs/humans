from django.urls import path
from django.conf import settings
from rsp.views import DashboardsView

app_name = 'rsp'

urlpatterns = [
    path('dashboard', DashboardsView.as_view(template_name = 'pages/rsp/Dashboard.html'), name='index'),

    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]