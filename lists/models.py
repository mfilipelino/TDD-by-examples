from django.db import models


class Item(models.Model):
    text = models.CharField(max_length=50, default='')
    list = models.ForeignKey('List', default=None, blank=True)


class List(models.Model):
    pass
