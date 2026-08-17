from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.homes.views import accessible_homes
from .services import simulate

@api_view(['POST'])
def run(request):
 homes=accessible_homes(request.user);home_id=request.data.get('home');home=homes.filter(id=home_id).first() if home_id else homes.first()
 if not home: return Response({'detail':'No hay un hogar accesible para simular.'},status=status.HTTP_404_NOT_FOUND)
 if not home.user_can_manage(request.user): return Response({'detail':'No tienes permisos para simular este hogar.'},status=status.HTTP_403_FORBIDDEN)
 try: steps=int(request.data.get('steps',1));seed=request.data.get('seed');seed=int(seed) if seed is not None else None
 except (TypeError,ValueError): return Response({'detail':'steps y seed deben ser enteros.'},status=status.HTTP_400_BAD_REQUEST)
 ids=simulate(home,steps,seed);return Response({'home':home.id,'steps':max(1,min(steps,100)),'telemetryCreated':len(ids),'telemetryIds':ids},status=status.HTTP_201_CREATED)
