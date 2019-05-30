from django.db import models

from reversion.models import Version

class HistoryManager(models.Manager):

    def all_record_logs(self, record):
        return Version.objects.get_for_object(record)

    def filter_record_logs(self, record, **kwargs):
        return Version.objects.get_for_object(record).filter(**kwargs)