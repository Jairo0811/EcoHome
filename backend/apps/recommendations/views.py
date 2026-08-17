from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from apps.homes.views import accessible_homes
from .models import Recommendation
from .serializers import RecommendationSerializer
from .services import generate_for_home

class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
 serializer_class=RecommendationSerializer
 def get_queryset(self): return Recommendation.objects.filter(home__in=accessible_homes(self.request.user),status=Recommendation.Status.ACTIVE)
 @action(detail=False,methods=['post'])
 def refresh(self,request):
  generated=[]
  for home in accessible_homes(request.user): generated.extend(generate_for_home(home))
  return Response(self.get_serializer(generated,many=True).data)
 @action(detail=True,methods=['post'])
 def dismiss(self,request,pk=None):
  rec=self.get_object()
  if not rec.home.user_can_manage(request.user): raise PermissionDenied('No tienes permisos para descartar recomendaciones.')
  rec.status=Recommendation.Status.DISMISSED;rec.save(update_fields=['status','generated_at']);return Response(self.get_serializer(rec).data)
 @action(detail=True,methods=['post'])
 def apply(self,request,pk=None):
  rec=self.get_object()
  if not rec.home.user_can_manage(request.user): raise PermissionDenied('No tienes permisos para marcar recomendaciones como aplicadas.')
  rec.status=Recommendation.Status.APPLIED;rec.save(update_fields=['status','generated_at']);return Response(self.get_serializer(rec).data)
