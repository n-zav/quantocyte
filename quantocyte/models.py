from django.db import models


class Item(models.Model):
    name = models.TextField(max_length=100, verbose_name="Name")
