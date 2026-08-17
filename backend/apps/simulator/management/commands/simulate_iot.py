from django.core.management.base import BaseCommand,CommandError
from apps.homes.models import Home
from apps.simulator.services import simulate

class Command(BaseCommand):
 help='Genera telemetría sintética para un hogar EcoHome.'
 def add_arguments(self,parser):
  parser.add_argument('--home',type=int,required=True);parser.add_argument('--steps',type=int,default=10);parser.add_argument('--seed',type=int,default=42)
 def handle(self,*args,**options):
  home=Home.objects.filter(id=options['home']).first()
  if not home: raise CommandError('Hogar no encontrado.')
  ids=simulate(home,options['steps'],options['seed']);self.stdout.write(self.style.SUCCESS(f'Simulación completada: {len(ids)} lecturas creadas.'))
