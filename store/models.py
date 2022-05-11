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
