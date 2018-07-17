from django.db import models
from django.db.models import Q
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.core.exceptions import ObjectDoesNotExist


class HistoricalObject(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    @property
    def updatedTime(self):
        try:
            return self.history.latest().history_date
        except ObjectDoesNotExist:
            return None

    @property
    def createdTime(self):
        try:
            return self.history.earliest().history_date
        except ObjectDoesNotExist:
            return None

    @property
    def updatedBy(self):
        try:
            return self.history.latest().history_user
        except ObjectDoesNotExist:
            return None

    @property
    def createdBy(self):
        try:
            return self.history.earliest().history_user
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return self.name


class Customer(HistoricalObject):
    history = HistoricalRecords()
    redmineLink = models.CharField(max_length=400, blank=True)


class System(HistoricalObject):
    history = HistoricalRecords()
    description = models.TextField(blank=True)
    customers = models.ManyToManyField(Customer, blank=True)


class Server(HistoricalObject):
    history = HistoricalRecords()
    link = models.CharField(max_length=400, blank=True)
    systems = models.ManyToManyField(System, blank=True)
    customers = models.ManyToManyField(Customer, blank=True)


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
    planned = models.NullBooleanField(blank=True, null=True)
    solution = models.TextField(blank=True)
    servers = models.ManyToManyField(Server, blank=True)
    systems = models.ManyToManyField(System, blank=True)
    history = HistoricalRecords()
    # createdTime
    # createdBy
    # updatedBy

    @property
    def updatedTime(self):
        try:
            return self.history.latest().history_date
        except ObjectDoesNotExist:
            return None

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
