from django.db import models

# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to="produtos/")
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return self.nome