from django.db import models
from django.contrib.auth.models import User
#for this, is needed to install PIL
from easy_thumbnails.fields import ThumbnailerImageField 
import datetime

class PostManager(models.Manager):
    def get_visible(self):
        return self.get_query_set().filter(publish_at__lte.datetime.now(), active = True)

class TimeStampedActivate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False, help_text="Item is live")
    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name



class Seller(models.Model):
    name = models.CharField(max_length=30)
    website = models.URLField()
    description = models.TextField(blank=True,
                                   help_text="Describe yourself.")
    user = models.ForeignKey(User, related_name="seller")
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        return self.name


class Product(TimeStampedActivate):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(Subcategory)
    description = models.TextField(blank=True, help_text="Describe product")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    seller = models.ForeignKey(Seller)
    slug = models.SlugField(max_length=80)
    publish_at = models.DateTimeField(default=datetime.datetime.now())
    photo = ThumbnailerImageField(upload_to="products",
			 blank=True,
			 resize_source = {'size': [185, 185],
			 'crop': 'smart'} ,)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-publish_at']
