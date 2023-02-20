from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cash = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class Purchase(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    available = models.PositiveSmallIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'

    def __str__(self):
        return f'{self.product}'

    def total(self):
        return self.product.price * self.available


class Return(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.purchase


