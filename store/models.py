from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.shortcuts import reverse
from django_resized import ResizedImageField


AVAILABILITY = (
    ('Y', 'Available'),
    ('N', 'Out of Stock'),
)


SIZES = (
    ('King', 'King - 108" x 120"'),
    ('Queen', 'Queen - 90" x 108"'),
    ('Single', 'Single'),
    ('Double', 'Double')
)

CATEGORY = (
    ('B', 'Bedsheet'),
    ('D', 'Dohar')
)


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Banner(BaseModel):
    image = models.ImageField(upload_to='banner', null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            this = Banner.objects.get(id=self.id)
            if this.image != self.image or this.image == 'clear':
                this.image.delete()
        except: pass
        super(Banner, self).save(*args, **kwargs)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)  
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)  
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Items(BaseModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=500)
    size = models.CharField(choices=SIZES, default=SIZES[0][0], max_length=10)
    category = models.CharField(choices=CATEGORY, default=CATEGORY[0][0], max_length=1)
    featured = models.BooleanField(default=False)
    availability = models.CharField(choices=AVAILABILITY, default=AVAILABILITY[0][0], max_length=1)
    image = ResizedImageField(upload_to="", null=True, blank=True)
    slug = models.SlugField(max_length=100)
    date_added = models.DateField(default=timezone.now)
    wishlist = models.ManyToManyField(User, related_name="wishlist", blank=True)

    def save(self, *args, **kwargs):
        try:
            this = Items.objects.get(id=self.id)
            if this.image != self.image or this.image == 'clear':
                this.image.delete()
        except: pass
        super(Items, self).save(*args, **kwargs)

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
    
    def get_add_to_wishlist_url(self):
        return reverse("store:add", kwargs={
            'slug': self.slug
        })

    def get_remove_wishlist_url(self):
        return reverse("store:remove", kwargs={
            'slug': self.slug
        })

    class Meta:
        verbose_name_plural = 'Products'


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
    
    class Meta:
        verbose_name_plural = 'Cart Items'


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey( 'Address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
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
    
    class Meta:
        verbose_name_plural = 'Orders'


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


class Payment(BaseModel):
    pass
