from rest_framework.viewsets import GenericViewSet


class MultiSerializerGenericViewSet(GenericViewSet):
    serializers = None

    def get_serializer_class(self):
        assert self.serializers is not None, (
            "'%s' should include a `serializers` attribute."
            % self.__class__.__name__
        )

        assert self.serializers.get('default') is not None, (
            "`serializers` should include a default serializer"
        )

        return self.serializers.get(self.action, self.serializers['default'])