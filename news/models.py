from django.db import models

# Create your models here.

class Article(models.Model):
  title = models.CharField(max_length=200)
  body = models.TextField()
  pub_date = models.DateTimeField("date published")

  def __str__(self):
    return self.title

class Comment(models.Model):
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  comment_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.comment_text

