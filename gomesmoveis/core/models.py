from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    destaque = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="produtos"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    

class ProdutoImagem(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="imagens"
    )

    imagem = models.ImageField(upload_to="produtos/")

    def clean(self):
        if self.produto and self.produto.pk:
            if self.produto.imagens.count() >= 4:
                raise ValidationError("Este produto já possui 4 imagens.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.produto.nome