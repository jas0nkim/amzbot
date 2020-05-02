from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())  # Apply any filter backends on the base queryset
        _filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                _filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **_filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
