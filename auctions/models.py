from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=48)

    def __str__(self):
        return self.category

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.TextField()
    bid = models.DecimalField(max_digits=6,decimal_places=2)
    image_url = models.URLField(max_length=512)
    sold = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category")
    categories = models.ManyToManyField(Category, blank=True, related_name="choose_categories")

    def __str__(self):
        return f"{self.user} is auctioning {self.title}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watchlist = models.BooleanField(default=False)

class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=6, decimal_places=2,default=False)

    def __str__(self):
        return f"bid on item: {self.listing} by {self.user} with bid: {self.bid}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()

