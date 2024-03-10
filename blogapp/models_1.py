from django.db import models

class WaterSupply(models.Model):
    value = models.IntegerField()
    date = models.DateField()
    description = models.TextField()

class SuspendedSolids(models.Model):
    value = models.IntegerField()
    date = models.DateField()
    description = models.TextField()

class AmmoniumNitrogen(models.Model):
    value = models.IntegerField()
    date = models.DateField()
    description = models.TextField()

class PhosphatePhosphorus(models.Model):
    value = models.IntegerField()
    date = models.DateField()
    description = models.TextField()

class SludgeVolumeIndex(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()

class SludgeDoseByVolume(models.Model):
    value = models.IntegerField()
    date = models.DateField()
    description = models.TextField()

class SludgeDoseByWeight(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()

class PumpFrequency(models.Model):
    value = models.IntegerField()
    date = models.DateField()
    description = models.TextField()

class DissolvedOxygen(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()

class Temperature(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()

class BODAtOutlet(models.Model):
    value = models.IntegerField()
    date = models.DateField()
    description = models.TextField()

class AmmoniumNitrogenAtOutlet(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()

class PhosphatePhosphorusAtOutlet(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()

class NitrateNitrogenAtOutlet(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()

class NitriteNitrogenAtOutlet(models.Model):
    value = models.FloatField()
    date = models.DateField()
    description = models.TextField()


