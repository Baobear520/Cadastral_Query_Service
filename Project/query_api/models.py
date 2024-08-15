from django.db import models


class Query(models.Model):
    """A model class for queries"""

    cadastral_number = models.CharField(max_length=32,unique=True)
    latitude = models.DecimalField(max_digits=6,decimal_places=3)
    longtitude = models.DecimalField(max_digits=6,decimal_places=3)
    result = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f"Query{self.id}"