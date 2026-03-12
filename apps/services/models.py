from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    full_description = models.TextField()
    price_display = models.CharField(max_length=100, blank=True)
    is_price_on_request = models.BooleanField(default=True)
    image = models.ImageField(upload_to="services/", blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})

