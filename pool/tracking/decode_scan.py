from .models import Track, TrackHistory
from django.utils import timezone
from django.contrib import messages
from .threads import DischargeThread
import threading
import json

THREADS = {}


class Command:
    def __init__(self, scann, request, queryset):
        self.scann = scann
        self.request = request
        self.queryset = queryset
        self.stop_thread = False
        self.discharge = None
        self.discharge_thread = None

    def create_thread(self, swimmer):
        settings = {'scann': self.scann, 'discharged': 2, 'step': 5}
        self.discharge = DischargeThread(settings, self)
        self.discharge_thread = threading.Thread(target=self.discharge.start_discharge, name=self.scann[1])
        THREADS[self.scann[1]] = [self.discharge, swimmer]
        print('test')
        return self.discharge_thread

    def decode_scann(self):
        if self.scann[0] == 'ZAW':
            self.zaw()
        elif self.scann[0] == 'TOR':
            self.tor()
        else:
            messages.error(self.request, 'Błędny format skanu')

    def zaw(self):
        if self.queryset.count() < 5:
            if not self.queryset.filter(swimmer=self.scann[1]).exists():
                track = self.queryset.filter(track__isnull=True).last()
                if track:
                    track.swimmer = self.scann[1]
                else:
                    track = Track(swimmer=self.scann[1])
                track.save()
            else:
                track = self.queryset.filter(swimmer=self.scann[1]).last()
                messages.error(self.request,
                               f'przerywam działanie na torze {track.track} oraz zawodnika {self.scann[1]}')
                track.delete()
                for scann, swimmer in THREADS.items():
                    if swimmer[1] == self.scann[1]:
                        swimmer[0].stop_thread()
                        del THREADS[scann]
                        break

        else:
            messages.error(self.request, 'Wszystkie tory zajęte')

    def tor(self):
        if len(self.scann) != 3:
            messages.error(self.request, 'Błędny format skanu')
        elif self.scann[2] == 'START':
            self.start_command()
        elif self.scann[2] == 'STOP':

            if self.scann[1] in THREADS:
                THREADS[self.scann[1]][0].stop_thread()
                self.stop_command(THREADS[self.scann[1]][0].get_history())
                del THREADS[self.scann[1]]

    def start_command(self):
        if 0 < int(self.scann[1].strip('0')) <= 5:

            if self.queryset.filter(track=self.scann[1]).first():
                messages.error(self.request, 'Tor zajęty')

            elif not self.queryset.filter(swimmer__isnull=False, track__isnull=True).exists():
                messages.error(self.request, 'Brak zawodnika na torze, zarejestruj zawodnika')

            else:
                free_track = self.queryset.filter(swimmer__isnull=False, track__isnull=True).last()
                free_track.track = self.scann[1]
                free_track.start_time = timezone.now().isoformat()
                free_track.stop_time = 'Trwa pomiar'
                free_track.status = 'Trwa pomiar'
                free_track.time = "Brak danych"
                free_track.save()
                thread = self.create_thread(free_track.swimmer)
                thread.start()

        else:
            messages.error(self.request, 'Nie ma takiego toru')

    def stop_command(self, history: list):
        if 0 < int(self.scann[1].strip('0')) <= 5:
            if not self.queryset.filter(track=self.scann[1]).exists():
                messages.error(self.request, 'Na torze nie ma zawodnika')

            elif self.queryset.filter(swimmer__isnull=False, track__isnull=False).exists():

                track = self.queryset.filter(track=self.scann[1], start_time__isnull=False).last()
                trackHist = TrackHistory(
                    swimmer=track.swimmer,
                    track=track.track,
                    start_time=track.start_time,
                    status="Pomiar Zakończony",
                    stop_time=timezone.now().isoformat(),
                    time=timezone.now() - track.start_time,
                    history=json.dumps(history)
                )
                trackHist.save()
                track.delete()

        else:
            messages.error(self.request, 'Nie ma takiego toru')