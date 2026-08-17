import os

from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response(
        {
            "status": "ok",
            "service": "EcoHome API",
            "version": os.getenv("APP_VERSION", "1.0.0"),
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def readiness(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return Response({"status": "ready", "database": "ok"})
    except Exception:
        return Response(
            {"status": "not_ready", "database": "unavailable"},
            status=503,
        )
