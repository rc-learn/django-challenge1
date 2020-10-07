from django.db import models

# Create your models here.

class Note(models.Model):
	name = models.CharField(max_length=255)
	datas = models.TextField(blank=True,null=True)
	created  = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('modified',)
		#order by name which  is a tuple