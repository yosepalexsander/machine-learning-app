from django.db import models

# Create your models here.


class SentimentModel(models.Model):
    reviewname = models.CharField(max_length=100)
    reviewtext = models.TextField()

    class Meta:
        def __unicode__(self):
            return u"%s" % self.reviewname
