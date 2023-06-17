from django.db import models

# Create your models here.


class UploadedFile(models.Model):
    file = models.ImageField(upload_to='sample/')
