from django.db import models

# Create your models here.


class SentimentReview(models.Model):
    review_name = models.CharField(max_length=100)
    review_text = models.TextField()
    sentiment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "%s" % self.review_name
