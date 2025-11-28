from django.conf import settings
from django.db import models

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} - {self.autor}" if self.autor else f"{self.titulo} - Autor desconhecido"
