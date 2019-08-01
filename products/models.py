from django.db import models
from django.shortcuts import reverse
from PIL import Image
# from django.utils import timezone
# Create your models here.


class Category(models.Model):
    title   = models.CharField(max_length=255, db_index=True)
    slug    = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:list_by_category', kwargs={'cat_slug':self.slug})

    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# LABEL_CHOICES = (
#     ('P', 'primary'),
#     ('D', '')
# )

class Product(models.Model):
    title       = models.CharField(max_length=255, db_index=True)
    slug        = models.SlugField(max_length=255, unique=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    desc        = models.TextField(blank=True)
    image       = models.ImageField(upload_to='product_img/', blank=True, null=True)
    in_stock    = models.IntegerField(default=50)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title
    
    def is_available(self):
        return self.in_stock > 0

    is_available.boolean = True # to get tick in admin list 

    def get_product_status(self):
        # if self.created > timezone.now()
        # return new limited bestseller
        pass
    
    def get_absolute_url(self):
        return reverse('products:prod_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 300 or img.height>300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)