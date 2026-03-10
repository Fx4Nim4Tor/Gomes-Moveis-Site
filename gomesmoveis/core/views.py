from django.shortcuts import render
from .models import Produto

# Create your views here.
def inicio(request):
    produtos_destaque = Produto.objects.filter(destaque=True)

    return render(request, "index.html", {
        "produtos_destaque": produtos_destaque
    })
    # return render(request,"index.html")

def adm(request):
    return render(request, "admin/admin.html")