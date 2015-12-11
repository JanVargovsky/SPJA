from django.db import models
from django.contrib.auth.models import User

#class CustomUser(User):
#    pass

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__( self ):
        return "{0} - {1}".format( self.name, self.price )