from django.db import models

# Create your models here.
# your_app/models.py
#from django.db import models

class AccessTokenBlacklist(models.Model):
    # The JTI is the unique identifier of the JWT
    jti = models.CharField(max_length=255, unique=True)
    # Store when the token was blacklisted
    blacklisted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.jti