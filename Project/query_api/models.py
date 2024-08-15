from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Query(models.Model):
    """A model class for queries"""

    cadastral_number = models.CharField(max_length=32,unique=True)
    latitude = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[
            MinValueValidator(Decimal(-90)), 
            MaxValueValidator(Decimal(90))
            ]
        )
    longitude = models.DecimalField(
        max_digits=7,
        decimal_places=4,
        validators=[
            MinValueValidator(Decimal(-180)), 
            MaxValueValidator(Decimal(180))
            ]
        )
    result = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f"Query{self.id}"