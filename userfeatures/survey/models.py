from django.db import models

# Create your models here.
class User(AbstractUser):
    pass


class Question(models.Model):
    question = models.CharField(max_length=200)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

