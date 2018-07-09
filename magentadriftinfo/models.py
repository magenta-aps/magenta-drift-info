from django.db import models
from django.db.models import Q
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Customer(models.Model):
    name = models.CharField(max_length=200)
    redmineLink = models.CharField(max_length=400, blank=True)
    history = HistoricalRecords()
    # createdTime
    # createdBy
    # updatedTime
    # updatedBy

    def __str__(self):
        return self.name


class System(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    customers = models.ManyToManyField(Customer, blank=True)
    history = HistoricalRecords()
    # createdTime
    # createdBy
    # updatedTime
    # updatedBy

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=400, blank=True)
    systems = models.ManyToManyField(System, blank=True)
    customers = models.ManyToManyField(Customer, blank=True)
    history = HistoricalRecords()
    # createdTime
    # createdBy
    # updatedTime
    # updatedBy

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    LEVEL = (
        (NONE, 'None'),
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (CRITICAL, 'Critical'),
    )
    level = models.IntegerField(choices=LEVEL, null=True, default=2)
    startTime = models.DateTimeField('start time')
    endTime = models.DateTimeField('end time', blank=True, null=True)
    planned = models.BooleanField()
    solution = models.TextField(blank=True)
    servers = models.ManyToManyField(Server, blank=True)
    systems = models.ManyToManyField(System, blank=True)
    history = HistoricalRecords()
    # createdTime
    # createdBy
    # updatedTime
    # updatedBy

    def __str__(self):
        return self.title

    def active(self):
        now = timezone.now()
        return self.startTime <= now <= self.endTime

    @staticmethod
    def filter_active(qs):
        now = timezone.now()
        return qs.filter(
            Q(endTime__gte=now) | Q(endTime__isnull=True),
            startTime__lte=now,
        )

    @staticmethod
    def filter_former(qs):
        now = timezone.now()
        return qs.filter(endTime__lte=now)

    @staticmethod
    def filter_future(qs):
        now = timezone.now()
        return qs.filter(startTime__gte=now)

    @staticmethod
    def filter_server(server):
        return server.events.objects.all()
