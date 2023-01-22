from django.contrib.contenttypes.models import ContentType
from django.db import models


class DataSource(models.Model):

    def test(self):
        DataImport(success=True).save()


class DataImport(models.Model):

    success = models.BooleanField(default=False)


class TransformMap(models.Model):

    datasource = models.ForeignKey('DataSource', on_delete=models.CASCADE)
    target = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    field_map = models.JSONField()

    def test(self):
        pass
