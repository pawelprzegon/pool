from .models import Track, TrackHistory
from django.views.generic import  ListView
from django.views.generic.edit import FormMixin
from .forms import ScanForm
from django.urls import reverse_lazy
from django.contrib import messages
from tracking.decode_scan import zaw, tor


class TrackStatusView(FormMixin, ListView):
    model = Track
    context_object_name = 'tracks'
    template_name = "tracking/home.html"
    form_class = ScanForm

    def get_success_url(self):
        return reverse_lazy("home")

    def decode_scan(self, scann):
        scann = scann.split('_')

        if scann[0] == 'ZAW':
            zaw(scann, self.request, queryset=super().get_queryset())
        elif scann[0] == 'TOR':
            tor(scann, self.request, queryset=super().get_queryset())
        else:
            messages.error(self.request, 'Błędny format skanu')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            scann = form.cleaned_data.get('scann')
            self.decode_scan(scann=scann)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TrackStatisticsView(ListView):
    model = TrackHistory
    context_object_name = 'tracks'
    template_name = "tracking/statistics.html"
