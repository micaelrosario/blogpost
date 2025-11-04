from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    conteudo = models.TextField('')

    def __str__(self):
        return self.titulo + ' | ' + str(self.autor)


