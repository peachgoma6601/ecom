from django.urls import reverse
from django.db import models

# Create your models here.

class Catagory(models.Model):
    catagory_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField(max_length=50,blank=True)
    catagory_image = models.ImageField(upload_to ='images/catagory',blank=True)

    class Meta:
        verbose_name = 'Catagory'
        verbose_name_plural = 'Catagories'

    def get_url(self):
        return reverse('products_by_catagory',args=[self.slug])
    def __str__(self):
        return self.catagory_name
