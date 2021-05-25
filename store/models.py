from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.shortcuts import reverse


AVAILABILITY = (
    ('Y', 'Available'),
    ('N', 'Out of Stock'),
)

class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User) #add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User) #add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Items(BaseModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField()
    description = models.TextField(max_length=200)
    label = models.CharField(choices=AVAILABILITY, default=AVAILABILITY[0][0], max_length=1)
    slug = models.SlugField(max_length=100)
    # image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={'slug': self.slug})


class Order(BaseModel):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.transaction_id)


class OrderItem(BaseModel):
    product = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

class ShippingAddress(BaseModel):
    name = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pincode = models.IntegerField()

    def __str__(self):
        return str(self.address)

class Payment(BaseModel):
    pass


class Refund(BaseModel):
    pass
