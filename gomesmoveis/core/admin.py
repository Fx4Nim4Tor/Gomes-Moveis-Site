from django.contrib import admin
from .models import Produto, Categoria, ProdutoImagem

admin.site.register(Categoria)

class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 3
    max_num = 3

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ProdutoImagemInline]