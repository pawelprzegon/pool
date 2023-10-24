from django.test import TestCase
from django.urls import reverse
from tracking.models import TrackHistory, Track
from django.utils import timezone
from ..factories import TrackStatusFactory, TrackStatisticsFactory


class TrackStatusViewTest(TestCase):
    def setUp(self):
        self.tracks = TrackStatusFactory
        self.tracks.create_batch(4)
        self.zaw_data = {
            "scann": "ZAW_Paweł Przegoń",
        }
        self.track_data = {
            "scann": "TOR_05_START"
        }

    def test_track_status(self):
        response = self.client.get(reverse('home'))
        track_qt = Track.objects.count()
        track = Track.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/home.html')
        self.assertEqual(track_qt, 4)
        self.assertEqual(track.swimmer, 'Johny Bravo')
        self.assertEqual(track.stop_time, 'Trwa pomiar')

    def test_add_swimmer(self):
        response = self.client.post(reverse('home'), data=self.zaw_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_add_track(self):
        response = self.client.post(reverse('home'), data=self.track_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_wrong_scann_form(self):
        response = self.client.post(reverse('home'), data={'bad_command': 'bad_command'})
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(response.status_code, 400)




# class TrackStatisticsViewTest(TestCase):
#     def setUp(self):
#         self.tracks = TrackStatusFactory()
#         self.tracks.create_batch(25)
#
#     def test_track_status(self):
#         response = self.client.get(reverse('statistics'))
#         self.assertEqual(response.status, 200)
#         self.assertTemplateUsed(response, 'tracking/statistics.html')
#
#     def test_post_track_status(self):
#         filtered_response = self.client.get(reverse('statistics'), data={'track': 1})
