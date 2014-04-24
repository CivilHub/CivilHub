from django.db import models

class Location(models.Model):
    """
    Basic location model
    """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.name
