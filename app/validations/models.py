from django.db import models


class IbanValidation(models.Model):
    iban = models.CharField(max_length=34)
    valid = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
