from rest_framework import serializers
from .models import Recommendation
class RecommendationSerializer(serializers.ModelSerializer):
 class Meta:
  model=Recommendation
  fields=['id','home','key','category','priority','title','description','estimated_savings_percent','status','generated_at']
  read_only_fields=fields
