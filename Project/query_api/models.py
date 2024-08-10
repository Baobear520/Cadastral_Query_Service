from django.db import models


class Query(models.Model):
    cadastral_number = models.IntegerField(max_length=12)
    latitude = models.DecimalField(max_digits=5,decimal_places=3)
    longtitude = models.DecimalField(max_digits=5,decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cadastral_number','latitude','longtitude'], 
                name='unique_property',
                violation_error_message="A property must have unique cadastral number, latitude and longtitude"
                )
        ]

class Results(models.Model):
    query = models.ForeignKey(Query,on_delete=models.CASCADE)
    result = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)