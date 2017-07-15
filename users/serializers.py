import datetime

import math
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
        ret['subscribed'] = False
        if instance in self.context['request'].user.subscribers.all():
            ret['subscribed'] = True
        return ret


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        filter_dict = self.context
        kwargs = {}

        last_year = {0: 12, -1: 11, -2: 10, -3: 9, -4: 8}
        current_month = datetime.datetime.now().month
        ret['evolution'] = {}
        for month in range(current_month, current_month - 5, -1):
            if month > 0:
                ret['evolution'][month] = self.calculate_yield(instance.bet_set.filter(month=month))
            else:
                ret['evolution'][last_year[month]] = self.calculate_yield(
                    instance.bet_set.filter(month=last_year[month]))

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

    def calculate_yield(self, bets):
        ret = {}
        ret['money_staked'] = 0.0
        ret['earnings'] = 0.0
        ret['losses'] = 0.0
        ret['benefit'] = 0
        ret['yield'] = 0
        if bets:
            for bet in bets:
                ret['money_staked'] = ret['money_staked'] + bet.amount
                if bet.status == 'W':
                    ret['earnings'] = ret['earnings'] + (bet.amount * bet.odds - bet.amount)
                elif bet.status == 'L':
                    ret['losses'] = ret['losses'] - bet.amount
            ret['benefit'] = ret['earnings'] + ret['losses']
            ret['yield'] = math.ceil((ret['benefit'] / ret['money_staked']) * 100*100)/100

        return ret['yield']
