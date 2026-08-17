import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.devices.models import Telemetry
from apps.homes.views import accessible_homes
from .services import dashboard_report


@api_view(['GET'])
def overview(request):
    try: days=int(request.query_params.get('days','30'))
    except ValueError: days=30
    return Response(dashboard_report(request.user,days))


@api_view(['GET'])
def consumption_csv(request):
    homes=accessible_homes(request.user)
    rows=Telemetry.objects.select_related('device','device__home').filter(device__home__in=homes).order_by('-recorded_at')[:5000]
    response=HttpResponse(content_type='text/csv; charset=utf-8');response['Content-Disposition']='attachment; filename="ecohome-consumption.csv"'
    writer=csv.writer(response);writer.writerow(['home','device','metric','value','unit','recorded_at'])
    for row in rows: writer.writerow([row.device.home.name,row.device.name,row.metric,row.value,row.unit,row.recorded_at.isoformat()])
    return response
