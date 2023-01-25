from django.db import models

# Create your models here.

class Category(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=255)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    rate = models.DecimalField(max_digits=10, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)