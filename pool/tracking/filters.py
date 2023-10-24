import django_filters
from .models import TrackHistory


class TorFilter(django_filters.FilterSet):
    class Meta:
        model = TrackHistory
        fields = ["track"]