from django.db import models


class Track(models.Model):
    track = models.PositiveIntegerField(unique=True, null=True, blank=True)
    swimmer = models.CharField(max_length=100)
    start_time = models.DateTimeField(null=True, blank=True)
    stop_time = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    time = models.CharField(max_length=30)


    def __str__(self):
        return f"{self.swimmer}, {self.track}, {self.start_time}"


class TrackHistory(models.Model):
    track = models.PositiveIntegerField()
    swimmer = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    time = models.DurationField()
