from django.db import models


class Series(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.DecimalField(max_digits=5, decimal_places=2)


class Branch(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Mileage(models.Model):
    series = models.ForeignKey(Series, on_delete=models.PROTECT, related_name='series_mileage')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='branch_mileage')
    year = models.IntegerField()
    value = models.IntegerField()