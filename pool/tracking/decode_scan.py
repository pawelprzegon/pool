from tracking.models import Track, TrackHistory
from django.utils import timezone
from django.contrib import messages


def zaw(scann, request, queryset):
    if not queryset.filter(swimmer=scann[1]).exists():
        track = queryset.filter(track__isnull=True).last()
        if track:
            track.swimmer = scann[1]
        else:
            track = Track(swimmer=scann[1])
        track.save()
    else:
        track = queryset.filter(swimmer=scann[1]).last()
        messages.error(request, f'przerywam działanie na torze {track.track} oraz zawodnika {scann[1]}')
        track.delete()


def tor(scann, request, queryset):
    if scann[2] == 'START':
        if 0 < int(scann[1].strip('0')) <= 5:

            if queryset.filter(track=scann[1]).first():
                messages.error(request, 'Tor zajęty')

            elif not queryset.filter(swimmer__isnull=False, track__isnull=True).exists():
                messages.error(request, 'Brak zawodnika na torze, zarejestruj zawodnika')

            else:
                free_track = queryset.filter(swimmer__isnull=False, track__isnull=True).last()
                free_track.track = scann[1]
                free_track.start_time = timezone.now()
                free_track.status = 'trwa pomiar'
                free_track.save()
        else:
            messages.error(request, 'Nie ma takiego toru')

    elif scann[2] == 'STOP':
        if 0 < int(scann[1].strip('0')) <= 5:
            if not queryset.filter(track=scann[1]).exists():
                messages.error(request, 'Na torze nie ma zawodnika')

            elif queryset.filter(swimmer__isnull=False, track__isnull=False).exists():

                track = queryset.filter(track=scann[1], start_time__isnull=False).last()
                trackHist = TrackHistory(
                    swimmer=track.swimmer,
                    track=track.track,
                    start_time=track.start_time,
                    status="Pomiar Zakończony",
                    stop_time=timezone.now(),
                    time=timezone.now() - track.start_time
                )
                trackHist.save()
                track.delete()

        else:
            messages.error(request, 'Nie ma takiego toru')