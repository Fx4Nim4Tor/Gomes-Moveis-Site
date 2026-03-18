from django.contrib import admin
from .models import Produto, Categoria, ProdutoImagem

class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nome",)}

admin.site.register(Categoria, CategoriaAdmin)

class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 3
    max_num = 3

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ProdutoImagemInline]