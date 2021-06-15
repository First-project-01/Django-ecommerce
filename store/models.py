from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.shortcuts import reverse
from django_resized import ResizedImageField

AVAILABILITY = (
    ('Y', 'Available'),
    ('N', 'Out of Stock'),
)


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Banner(BaseModel):
    image = ResizedImageField(upload_to='banner', null=True)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)  # add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Items(BaseModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField()
    description = models.TextField(max_length=200)
    label = models.CharField(choices=AVAILABILITY, default=AVAILABILITY[0][0], max_length=1)
    slug = models.SlugField(max_length=100)
    discount_price = models.FloatField(max_length=100, blank=True, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("store:add-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(BaseModel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Cart(BaseModel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    # 'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_items(self):
        total = 0
        for item in self.items.all():
            total = sum(item.quantity)
        return total

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=500, null=True)
    phone = models.CharField(max_length=10, null=False)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=100, null=False)
    default = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Refund(BaseModel):
    pass


class Payment(BaseModel):
    pass
