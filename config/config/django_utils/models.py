import uuid as uuid_lib

from django.db import models
from django_extensions.db.models import TimeStampedModel


class UUIDTimeStampModel(TimeStampedModel):
    id = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        primary_key=True
    )

    class Meta:
        abstract = True
