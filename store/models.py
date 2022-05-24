from django.urls import reverse
from django.db import models
from ecom1.models import Catagory

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50,unique=True)
    description = models.CharField(max_length=50,blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='media/Products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail',args=[self.catagory.slug,self.slug])


class ProductVariationManager(models.Manager):
    def colors(self):
        return super(ProductVariationManager, self).filter(variation_catagory='color',is_active=True)
    
    def sizes(self):
        return super(ProductVariationManager, self).filter(variation_catagory='size',is_active=True)

product_variation_choices = (
    ('color','color'),
    ('size','size'),
)


class ProductVariation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_catagory = models.CharField(max_length=50,choices=product_variation_choices)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = ProductVariationManager()
    
    def __str__(self):
        return self.variation_value