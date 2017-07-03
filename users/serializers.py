from rest_framework import serializers

from bets.serializers import BetSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['bets'] = BetSerializer(instance.bet_set, many=True).data
        return ret


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        filter_dict = self.context
        kwargs = {}
        for filter_field in filter_dict:
            kwargs['{}'.format(filter_field)] = filter_dict[filter_field]
        bets = instance.bet_set.filter(**kwargs)
        ret['money_staked'] = 0.0
        ret['earnings'] = 0.0
        ret['losses'] = 0.0
        ret['bets_number'] = bets.count()
        ret['win_bets'] = 0
        ret['lost_bets'] = 0
        ret['null_bets'] = 0
        ret['pending_bets'] = 0
        ret['benefit'] = 0
        ret['success_percentage'] = 0
        ret['yield'] = 0
        ret['odds_mean'] = 0
        ret['bets_mean'] = 0

        if bets:
            for bet in bets:
                ret['money_staked'] = ret['money_staked'] + bet.amount
                ret['odds_mean'] = ret['odds_mean'] + bet.odds
                if bet.status == 'W':
                    ret['earnings'] = ret['earnings'] + (bet.amount * bet.odds - bet.amount)
                    ret['win_bets'] = ret['win_bets'] + 1
                elif bet.status == 'L':
                    ret['losses'] = ret['losses'] - bet.amount
                    ret['lost_bets'] = ret['lost_bets'] + 1
                elif bet.status == 'N':
                    ret['null_bets'] = ret['null_bets'] + 1
                elif bet.status == 'P':
                    ret['pending_bets'] = ret['pending_bets'] + 1
            ret['benefit'] = ret['earnings'] + ret['losses']
            if ret['win_bets'] + ret['lost_bets'] > 0:
                ret['success_percentage'] = (ret['win_bets'] / (ret['win_bets'] + ret['lost_bets'])) * 100
            ret['yield'] = (ret['benefit'] / ret['money_staked']) * 100
            ret['odds_mean'] = ret['odds_mean'] / ret['bets_number']
            ret['bets_mean'] = ret['money_staked'] / ret['bets_number']
        return ret
