from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Classification(models.Model):
    classification = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.classification

class Travel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classification = models.ForeignKey(Classification, blank=True, null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField(default=datetime.now)
    finish_date = models.DateTimeField(default=datetime.now)
    evaluate = models.IntegerField(blank=True, null=True, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    def __str__(self):
        return '{} - {} - {}'.format(self.id, self.user.username, self.classification)
