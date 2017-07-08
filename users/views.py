from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from TFM_Backend.viewsets import MultiSerializerGenericViewSet
from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, UserStatsSerializer
from django_filters import rest_framework as filters


class UserViewSet(MultiSerializerGenericViewSet, ListModelMixin, UpdateModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializers = {
        'default': UserSerializer,
        'retrieve': UserDetailSerializer
    }
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.user.pk is instance.pk:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response({'Error', 'Can\'t update other user'}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def subscribe(self, request, pk=None):
        request.user.subscribers.add(self.get_object())
        return Response({'Ok': 'User subscribe correctly'})

    @detail_route(methods=['post'])
    def unsubscribe(self, request, pk=None):
        request.user.subscribers.remove(self.get_object())
        return Response({'Ok': 'User unsubscribe correctly'})

    @detail_route(methods=['get'])
    def stats(self, request, pk=None):
        filter = {}
        if request.query_params.get('month_year'):
            filter['month_year'] = request.query_params.get('month_year')
        if request.query_params.get('account'):
            filter['account'] = request.query_params.get('account')
        if request.query_params.get('tipster'):
            filter['tipster'] = request.query_params.get('tipster')
        data = UserStatsSerializer(User.objects.filter(pk=pk).first(), context=filter).data
        return Response({'data': data}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def my_stats(self, request):
        filter = {}
        if request.query_params.get('month_year'):
            filter['month_year'] = request.query_params.get('month_year')
        if request.query_params.get('account'):
            filter['account'] = request.query_params.get('account')
        if request.query_params.get('tipster'):
            filter['tipster'] = request.query_params.get('tipster')
        data = UserStatsSerializer(User.objects.filter(pk=request.user.pk).first(), context=filter).data
        return Response(data, status=status.HTTP_200_OK)
