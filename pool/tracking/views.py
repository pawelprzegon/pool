from .models import Track, TrackHistory
from django.views.generic import  ListView
from django.views.generic.edit import FormMixin
from .forms import ScanForm
from django.urls import reverse_lazy
from .decode_scan import Command
from .filters import TorFilter
from django.http import HttpResponseBadRequest


class TrackStatusView(FormMixin, ListView):
    model = Track
    context_object_name = 'tracks'
    template_name = "tracking/home.html"
    form_class = ScanForm
    ordering = ['-start_time']

    def get_success_url(self):
        return reverse_lazy("home")

    def decode_scan(self, scann):
        scann = scann.split('_')
        command = Command(scann, self.request, queryset=super().get_queryset())
        command.decode_scann()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            scann = form.cleaned_data.get('scann')
            self.decode_scan(scann=scann)
            return self.form_valid(form)
        else:
            return HttpResponseBadRequest("Niepoprawny formularz")


class TrackStatisticsView(ListView):
    model = TrackHistory
    context_object_name = 'tracks'
    template_name = "tracking/statistics.html"
    ordering = ['-start_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        for track in queryset:
            if track.time:
                track.time = str(track.time)[:-4]

        return TorFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        in_progress = Track.objects.all().order_by('-start_time')
        context['tracks_in_progress'] = in_progress
        context["tor_filter"] = TorFilter(
            self.request.GET, queryset=super().get_queryset()
        )
        return context

