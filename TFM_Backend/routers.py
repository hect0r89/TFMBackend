from rest_framework.routers import DefaultRouter

from accounts.views import AccountViewSet
from authentication.views import AuthenticationViewSet
from bets.views import BetViewSet
from users.views import UserViewSet

router = DefaultRouter()

#Assign the view and register the route
router.register(r'bets', BetViewSet, 'bets')
router.register(r'users', UserViewSet, 'users')
router.register(r'accounts', AccountViewSet, 'accounts')
router.register(r'authentication', AuthenticationViewSet, 'authentication')
