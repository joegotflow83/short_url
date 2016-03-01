from django.db import models
from django.contrib.auth.models import User
import uuid


# Helper Function
def random_url():
    """Generate a random url if none is supplied by the user"""
    pattern = uuid.uuid4()
    pattern = str(pattern)
    return pattern


class URL(models.Model):


    user = models.ForeignKey(User, default=1)
    url = models.URLField()
    short = models.CharField(max_length=255, default=random_url())
    description = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        """Prettify output"""
        return self.url
