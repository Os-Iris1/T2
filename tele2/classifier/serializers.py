from rest_framework import serializers
from classifier.data.model import ChurnData

class ChurnDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurnData
        fields = '__all__' 
        