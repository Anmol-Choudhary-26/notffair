from django.db import models
import uuid
from django.core.exceptions import ValidationError

# Create your models here.

def validate_image(image):
    file_size = image.file.size
    limit_kb = 200
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

class Store(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    productName = models.CharField(max_length=100 , null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=100 ,null= True)
    clubName = models.CharField(max_length=100 ,null=False)
    payment = models.CharField(max_length=100 ,null=False)

    def __str__(self):
        return self.productName
        
class ProductImage(models.Model):
    product = models.ForeignKey(Store, on_delete=models.CASCADE)
    prodimage = models.ImageField('pordimage',validators=[validate_image], null = True, blank= True)
    prodimageUrl = models.URLField(max_length=250,blank=True,null=True)

    def __str__(self):
        return f'{self.product}\'s image'