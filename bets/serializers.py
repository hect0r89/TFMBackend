from rest_framework import serializers

from bets.models import Bet


class BetSerializer(serializers.ModelSerializer):
    """
    Serializer for Bet model
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Bet
        fields = '__all__'
