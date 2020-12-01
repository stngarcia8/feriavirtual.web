import uuid
import datetime
from django.db import models


class Offer(models.Model):
    "Representa la oferta de un producto."
    OfferId = models.CharField(max_length=40, blank=True, null=True)
    Description = models.CharField(max_length=100, blank=True, null=True)
    Discount = models.FloatField(default=0)
    OfferType = models.IntegerField(default=0)
    TypeDescription = models.CharField(max_length=100, blank=True, null=True)
    PublishDate = models.DateField(default=datetime.date.today)
    Status = models.IntegerField(default=0)
    StatusDescription = models.CharField(max_length=40, blank=True, null=True)


class OfferDetail(models.Model):
    "Representa el detalle de la oferta."
    OfferDetailId = models.CharField(max_length=40, blank=True, null=True)
    Offer = models.ForeignKey(Offer, null=True, on_delete=models.CASCADE)
    OfferId = models.CharField(max_length=40, blank=True, null=True)
    ProductId = models.CharField(max_length=40, blank=True, null=True)
    ProductName = models.CharField(max_length=50, blank=True, null=True)
    ActualValue = models.FloatField(default=0)
    Percent = models.CharField(max_length=10, blank=True, null=True)
    OfferValue = models.FloatField(max_length=10, blank=True, null=True) 

    def save(self, *args, **kwargs):
        self.OfferId = self.Offer.OfferId
        super(OfferDetail, self).save(*args, **kwargs)