from django.test import TestCase
from django.urls import reverse
from tracking.models import TrackHistory, Track
from datetime import datetime
from ..factories import TrackStatusFactory, TrackStatisticsFactory


class TrackStatusViewTest(TestCase):
    def setUp(self):
        self.tracks = TrackStatusFactory
        self.tracks.create_batch(1)
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
        self.assertEqual(track_qt, 1)
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
        response = self.client.post(reverse('home'), data={'scann': 'bad_command'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))
        self.assertIn('messages', response.context)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Błędny format skanu')

    def test_add_over_swimmer(self):
        self.tracks.create_batch(4)
        response = self.client.post(reverse('home'), data={'scann': 'ZAW_Test User'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Wszystkie tory zajęte')

    def test_scann_used_track(self):
        self.tracks.create_batch(1, track=1)
        response_swimmer = self.client.post(reverse('home'), data=self.zaw_data)
        self.assertEqual(response_swimmer.status_code, 302)

        response = self.client.post(reverse('home'), data={'scann': 'TOR_01_START'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Tor zajęty')

    def test_scann_track_before_scann_swimmer(self):
        response = self.client.post(reverse('home'), data={'scann': 'TOR_01_START'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Brak zawodnika na torze, zarejestruj zawodnika')

    def test_swimmer_scann_second_time(self):
        response_swimmer = self.client.post(reverse('home'), data=self.zaw_data)
        swimmer = Track.objects.last()
        self.assertEqual(response_swimmer.status_code, 302)
        self.assertEqual(swimmer.swimmer, 'Paweł Przegoń')


class TrackStatisticsViewTest(TestCase):
    def setUp(self):
        self.tracks = TrackStatisticsFactory
        self.tracks.create_batch(5)

    def test_track_status(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/statistics.html')

    def test_track_have_stop_time(self):
        track = TrackHistory.objects.first()
        self.assertIsInstance(track.stop_time, datetime)

    def test_post_track_status(self):
        self.tracks.create_batch(5, track=1)
        filtered_response = self.client.get(reverse('statistics') + '?track=1')
        self.assertEqual(filtered_response.status_code, 200)
        self.assertEqual(len(filtered_response.context['tracks']), 6)

        self.tracks.create_batch(5, track=2)
        filtered_response = self.client.get(reverse('statistics') + '?track=2')
        self.assertEqual(filtered_response.status_code, 200)
        self.assertEqual(len(filtered_response.context['tracks']), 6)