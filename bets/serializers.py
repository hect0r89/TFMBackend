from rest_framework import serializers

from accounts.models import Account
from bets.models import Bet


class BetSerializer(serializers.ModelSerializer):
    """
    Serializer for Bet model
    """
    class Meta:
        model = Bet
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['username'] = instance.user.username
        return ret


class BetUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Bet
        fields = '__all__'

    def validate_account(self, value):
        if value:
            if value.user.pk == self.context['request'].user.pk:
                return value
            else:
                raise serializers.ValidationError("Account belongs to other user")

    def validate_amount(self, value):
        if value:
            if value > 0:
                return value
            else:
                raise serializers.ValidationError("Amount must be greater than 0")

