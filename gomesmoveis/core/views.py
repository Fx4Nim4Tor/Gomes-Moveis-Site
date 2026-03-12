from django.shortcuts import render, get_object_or_404
from .models import Produto

# Create your views here.
def inicio(request):
    produtos_destaque = Produto.objects.filter(destaque=True)

    return render(request, "index.html", {
        "produtos_destaque": produtos_destaque
    })
    # return render(request,"index.html")


def produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)

    return render(request, "produto.html", {
        "produto": produto
    })



# nao sendo usado no momento
def adm(request):
    return render(request, "admin/admin.html")