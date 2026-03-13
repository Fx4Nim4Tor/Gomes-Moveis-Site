from django.shortcuts import render, get_object_or_404
from .models import Produto

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
        .order_by("?")[:5]                     # aleatório e limitado a 5
    )

    return render(request, "produto.html", {
        "produto": produto,
        "produtos_relacionados": produtos_relacionados
    })



# nao sendo usado no momento
def adm(request):
    return render(request, "admin/admin.html")