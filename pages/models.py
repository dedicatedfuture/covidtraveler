from django.db import models

# Create your models here.
class RecentNewsArticles(models.Model):
	title = models.CharField(max_length=200)
	link = models.CharField(max_length=2048)
	desc = models.TextField(null=True, blank=True)
	date = models.DateTimeField()