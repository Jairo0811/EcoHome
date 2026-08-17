from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies=[('homes','0003_homemembership')]
    operations=[migrations.CreateModel(name='Recommendation',fields=[
      ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
      ('key',models.CharField(max_length=160)),('category',models.CharField(choices=[('ENERGY','Energía'),('WATER','Agua'),('GAS','Gas'),('DEVICES','Dispositivos'),('SECURITY','Seguridad')],max_length=20)),('priority',models.CharField(choices=[('LOW','Baja'),('MEDIUM','Media'),('HIGH','Alta')],default='MEDIUM',max_length=16)),('title',models.CharField(max_length=180)),('description',models.TextField()),('estimated_savings_percent',models.PositiveSmallIntegerField(default=0)),('status',models.CharField(choices=[('ACTIVE','Activa'),('DISMISSED','Descartada'),('APPLIED','Aplicada')],default='ACTIVE',max_length=16)),('generated_at',models.DateTimeField(auto_now=True)),('home',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='recommendations',to='homes.home'))],options={'ordering':['-generated_at']}),migrations.AddConstraint(model_name='recommendation',constraint=models.UniqueConstraint(fields=('home','key'),name='uq_home_recommendation_key'))]
