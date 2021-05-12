from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserModel.objects.create(user=kwargs['instance'])
    post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)


class UserModel(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Items(BaseModel):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    # image = models.ImageField()

    def __str__(self):
        return self.title


class CartItems(BaseModel):
    pass


class ShoppingCart(BaseModel):
    pass


class Address(BaseModel):
    pass


class Payment(BaseModel):
    pass


class Refund(BaseModel):
    pass
