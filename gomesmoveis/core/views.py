from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Produto, Categoria
from django.template.loader import render_to_string
from django.http import JsonResponse
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


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



def produtos(request):
    lista_produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    tipo_produtos = Produto.TIPOS

    #filtra por categoria
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
    
    #Verifica se não tem nenhum filtro ativo
    sem_filtro = not categorias_selecionadas and not tipos_selecionados
    # Detecta se é a primeira página (page=1 ou sem page na URL)
    page_number = request.GET.get('page', 1)

    if sem_filtro:
        ids = list(lista_produtos.values_list('id', flat=True))

        # Se for page=1 ou primeira vez, gera nova ordem aleatória e salva na sessão
        if str(page_number) == '1':
            random.shuffle(ids)
            request.session['ordem_produtos'] = ids

        # Usa a ordem salva na sessão (se existir), senão embaralha
        ids_ordenados = request.session.get('ordem_produtos') or ids
        
        # Preserva a ordem aleatória usando CASE WHEN no banco
        from django.db.models import Case, When, IntegerField
        ordering = Case(
            *[When(id=id_, then=pos) for pos, id_ in enumerate(ids_ordenados)],
            output_field=IntegerField()
        )
        lista_produtos = lista_produtos.order_by(ordering)

    paginator = Paginator(lista_produtos, 12)  #usa a lista filtrada
    # page_number = request.GET.get('page')
    itens = paginator.get_page(page_number)

    # Se for requisição AJAX, retorna só os cards + info de paginação
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/cards_produtos.html', {'produtos': itens}, request=request)
        return JsonResponse({
            'html': html,
            'tem_proxima': itens.has_next(),
            'proxima_pagina': itens.next_page_number() if itens.has_next() else None,
        })

    return render(request, "produtos.html", {
        "produtos": itens,
        "categorias": categorias,
        "tipos": tipo_produtos,
    })


def buscar(request):
    query = request.GET.get('q', '').strip()
    resultados = []

    if query:
        produtos = Produto.objects.filter(
            nome__icontains=query  # busca pelo nome, ignorando maiúsculas
        )[:6]  # limita a 6 resultados no dropdown

        resultados = [
            {
                'nome': p.nome,
                'slug': p.slug,
                'imagem': p.imagens.first().imagem.url if p.imagens.first() else None,
            }
            for p in produtos
        ]

    return JsonResponse({'resultados': resultados})





# ADEMIRO TELAS
def adm_login(request):
    erro = None

    if request.user.is_authenticated:
        return redirect('adm_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # só superusuário acessa
            login(request, user)
            return redirect('adm_dashboard')
        else:
            erro = 'Usuário ou senha inválidos.'

    return render(request, 'adm/login.html', {'erro': erro})


def adm_logout(request):
    logout(request)
    return redirect('adm_login')


@login_required(login_url='/adm/login/')  # redireciona para login se não estiver logado
def adm_dashboard(request):
    return render(request, 'adm/dashboard.html')


# cadastrar categorias
@login_required(login_url='/adm/login/')
def adm_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'adm/categorias.html', {'categorias': categorias})


@login_required(login_url='/adm/login/')
def adm_categoria_criar(request):
    erro = None

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        if not nome:
            erro = 'O nome é obrigatório.'
        elif Categoria.objects.filter(nome=nome).exists():
            erro = 'Já existe uma categoria com esse nome.'
        else:
            Categoria.objects.create(nome=nome)
            return redirect('adm_categorias')

    return render(request, 'adm/categoria_form.html', {'erro': erro, 'acao': 'Criar'})


@login_required(login_url='/adm/login/')
def adm_categoria_editar(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    erro = None

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        if not nome:
            erro = 'O nome é obrigatório.'
        elif Categoria.objects.filter(nome=nome).exclude(id=id).exists():
            erro = 'Já existe uma categoria com esse nome.'
        else:
            categoria.nome = nome
            categoria.save()
            return redirect('adm_categorias')

    return render(request, 'adm/categoria_form.html', {
        'erro': erro,
        'acao': 'Editar',
        'categoria': categoria
    })


@login_required(login_url='/adm/login/')
def adm_categoria_deletar(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        categoria.delete()
        return redirect('adm_categorias')

    return render(request, 'adm/categoria_confirmar_deletar.html', {'categoria': categoria})