from django.urls import path
from .views import consumption_csv,overview
urlpatterns=[path('overview/',overview,name='reports-overview'),path('consumption.csv',consumption_csv,name='reports-consumption-csv')]
