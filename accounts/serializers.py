from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Account model
    """

    class Meta:
        model = Account
        fields = '__all__'
