from rest_framework import serializers

from bets.models import Bet


class BetSerializer(serializers.ModelSerializer):
    """
    Serializer for Bet model
    """
    class Meta:
        model = Bet
        fields = '__all__'
