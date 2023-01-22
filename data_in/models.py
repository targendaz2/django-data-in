from django.contrib.contenttypes.models import ContentType
from django.db import models

CADENCE_CHOICES = [
    ('D', 'Daily'),
    ('W', 'Weekly'),
    ('B', 'Bi-weekly'),
    ('M', 'Monthly'),
]

DAY_NAME_CHOICES = [
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
]


class DataSource(models.Model):

    url = models.URLField()

    def test(self):
        DataImport(success=True).save()


class DataImport(models.Model):

    success = models.BooleanField(default=False)


class TransformMap(models.Model):

    datasource = models.ForeignKey('DataSource', on_delete=models.CASCADE)
    target = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    field_map = models.JSONField()

    def test(self):
        target_object = self.target.model_class()()

        for key, value in self.field_map.items():
            setattr(target_object, key, value)

        target_object.full_clean()
        target_object.save()


class ScheduledImport(models.Model):

    transform_map = models.ForeignKey('TransformMap', models.CASCADE)
    cadence = models.CharField(max_length=1, choices=CADENCE_CHOICES)
    day = models.IntegerField(choices=DAY_NAME_CHOICES)
    time = models.TimeField()
