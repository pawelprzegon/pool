import factory
from tracking.models import Track, TrackHistory
from django.utils import timezone


class TrackStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Track

    track = factory.Sequence(lambda n: n)
    swimmer = 'Johny Bravo'
    start_time = timezone.now()
    stop_time = 'Trwa pomiar'
    status = 'Trwa pomiar'
    time = "Brak danych"


class TrackStatisticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TrackHistory

    track = factory.Sequence(lambda n: n)
    swimmer = 'Johny Bravo'
    start_time = timezone.now()
    stop_time = timezone.now()
    status = 'Trwa pomiar'
    time = timezone.now() - timezone.now()