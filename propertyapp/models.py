from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Login(AbstractUser):
    is_tenant = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)


class Tenant(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='tenant')
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    image = models.FileField(upload_to='media/')


class Agent(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='agent')
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()


class TenantFeedback(models.Model):
    user = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant')
    date = models.DateField(auto_now=True)
    feedback = models.TextField()
    reply = models.CharField(max_length=300, null=True, blank=True)


class Property(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='property')
    image = models.FileField(upload_to='media/')
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    bed_no = models.CharField(max_length=100)
    bath_no = models.CharField(max_length=100)
    details = models.TextField()
    price = models.CharField(max_length=100)
    status_available = models.BooleanField(default=0)


class AddToCart(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenantid')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='propertyid')
    cart_status = models.BooleanField(default=0)


class BuyNow(models.Model):
    user = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='userid')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_id')
    totalprice = models.IntegerField()
    buynow_status = models.BooleanField(default=0)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    post = models.CharField(max_length=6)


class Payment(models.Model):
    buynowProperty = models.ForeignKey(BuyNow, on_delete=models.CASCADE, related_name='buynow')
    cardnumber = models.CharField(max_length=19)
    cvv = models.CharField(max_length=3)
    expiry_date = models.CharField(max_length=7)
