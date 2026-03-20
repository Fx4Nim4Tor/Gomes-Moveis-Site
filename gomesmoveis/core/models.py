from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os
# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            i = 1
            # garante que o slug seja único
            while Categoria.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    

class Produto(models.Model):
    TIPOS = [
        ("cadeira","Cadeira"),
        ("mesa","Mesa"),
        ("longarina","Longarina"),
        ("roupeiro","Roupeiro"),
        ("arquivo","Arquivos"),
        ("armario","Armários"),
        ("outros", "Outros")
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    destaque = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="outros")


    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="produtos"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            i = 1
            # garante que o slug seja único
            while Produto.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
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
            if self.produto.imagens.count() >= 3:
                raise ValidationError("Este produto já possui 3 imagens.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.imagem and os.path.isfile(self.imagem.path):
            os.remove(self.imagem.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.produto.nome