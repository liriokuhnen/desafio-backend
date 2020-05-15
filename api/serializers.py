from rest_framework import serializers

from api.models import Travel

class TravelSerialization(serializers.ModelSerializer):

    class Meta:
        model = Travel
        
        fields = [
            'id',
            'start_date',
            'finish_date',
            'classification',
            'evaluate'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'start_date': {'read_only': True},
            'finish_date': {'read_only': True},
        }

class TravelCreateSerialization(serializers.ModelSerializer):

    class Meta:
        model = Travel
        
        fields = [
            'id',
            'user',
            'start_date',
            'finish_date',
            'classification',
            'evaluate'
        ]
