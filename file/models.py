from django.db import models
import cloudinary
import cloudinary.uploader


# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to="uploads/")
    url = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.url)

    def save(self, *args, **kwargs):

        if self.file:
            rci = cloudinary.uploader.upload(self.file, resource_type="raw")
            self.url = rci["url"]
            self.file = None

        super().save(*args, **kwargs)
