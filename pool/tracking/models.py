from django.db import models


class Track(models.Model):
    swimmer = models.CharField(max_length=100)
    track = models.PositiveIntegerField(unique=True, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.swimmer}, {self.track}, {self.start_time}"


class TrackHistory(models.Model):
    swimmer = models.CharField(max_length=100)
    track = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    stop_time = models.DateTimeField()
    time = models.DurationField()
