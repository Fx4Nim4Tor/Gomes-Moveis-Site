from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Produto, Categoria
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.
def inicio(request):
    produtos_destaque = Produto.objects.filter(destaque=True)

    return render(request, "index.html", {
        "produtos_destaque": produtos_destaque
    })


def produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)

    produtos_relacionados = (
        Produto.objects
        .filter(categoria=produto.categoria)   # mesma categoria
        .exclude(id=produto.id)                # remove o produto atual
        .order_by("?")[:4]                     # aleatório e limitado a 5
    )

    return render(request, "produto.html", {
        "produto": produto,
        "produtos_relacionados": produtos_relacionados
    })

from django.core.paginator import Paginator


#para colocar os produtos na pagina onde mostra todos os produtos
def produtos(request):
    lista_produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    tipo_produtos = Produto.TIPOS

    # filtra por categoria se tiver
    categorias_selecionadas = request.GET.getlist('categoria')
    if categorias_selecionadas:
        lista_produtos = lista_produtos.filter(
            categoria__slug__in=categorias_selecionadas
        )

     # filtro tipo
    tipos_selecionados = request.GET.getlist('tipo')
    if tipos_selecionados:
        lista_produtos = lista_produtos.filter(
            tipo__in=tipos_selecionados
        )

    # paginator = Paginator(lista_produtos, 12)  #usa a lista filtrada
    # page_number = request.GET.get('page')
    # itens = paginator.get_page(page_number)


    return render(request, "produtos.html", {
        "produtos": lista_produtos,
        "categorias": categorias,
        "tipos": tipo_produtos,
    })




# nao sendo usado no momento
def adm(request):
    return render(request, "admin/admin.html")
