from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Produto, Categoria, ProdutoImagem
from django.template.loader import render_to_string
from django.http import JsonResponse
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'}


def validar_imagens_upload(imagens):
    for imagem in imagens:
        content_type = getattr(imagem, 'content_type', '')
        if not content_type.startswith('image/'):
            return 'Formato de imagem inválido. Envie apenas arquivos de imagem.'

        if '.' not in imagem.name:
            return 'Formato de imagem inválido. Envie um arquivo de imagem com extensão.'

        extension = imagem.name.rsplit('.', 1)[1].lower()
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            return 'Formato de imagem inválido. Envie JPG, PNG, GIF ou WEBP.'

        try:
            img = Image.open(imagem)
            img.verify()
        except Exception:
            return 'Arquivo enviado não é uma imagem válida.'
        finally:
            try:
                imagem.seek(0)
            except Exception:
                pass

    return None


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



def sobre(request):
    return render(request, "sobre.html")




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

    return render(request, 'adm/categorias.html', {'categorias': categorias, 'erro': erro, 'acao': 'Criar'})


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





# PRODUTOS
@login_required(login_url='/adm/login/')
def adm_produtos(request):
    produtos = Produto.objects.prefetch_related('imagens').select_related('categoria').all()
    return render(request, 'adm/produtos.html', {'produtos': produtos})


@login_required(login_url='/adm/login/')
def adm_produto_criar(request):
    categorias = Categoria.objects.all()
    erro = None

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        tipo = request.POST.get('tipo', '')
        categoria_id = request.POST.get('categoria')
        destaque = request.POST.get('destaque') == 'on'
        imagens = request.FILES.getlist('imagens')

        if not nome or not descricao or not categoria_id:
            erro = 'Nome, descrição e categoria são obrigatórios.'
        elif len(imagens) > 3:
            erro = 'Você pode enviar no máximo 3 imagens.'
        else:
            erro = validar_imagens_upload(imagens)

        if not erro:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            produto = Produto.objects.create(
                nome=nome,
                descricao=descricao,
                tipo=tipo,
                categoria=categoria,
                destaque=destaque,
            )
            for imagem in imagens:
                ProdutoImagem.objects.create(produto=produto, imagem=imagem)

            return redirect('adm_produtos')

    return render(request, 'adm/produto_form.html', {
        'categorias': categorias,
        'tipos': Produto.TIPOS,
        'erro': erro,
        'acao': 'Criar',
    })


@login_required(login_url='/adm/login/')
def adm_produto_editar(request, id):
    produto = get_object_or_404(Produto, id=id)
    categorias = Categoria.objects.all()
    erro = None

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        tipo = request.POST.get('tipo', '')
        categoria_id = request.POST.get('categoria')
        destaque = request.POST.get('destaque') == 'on'
        imagens_novas = request.FILES.getlist('imagens')
        imagens_deletar = request.POST.getlist('deletar_imagem')  # ids das imagens a remover

        if not nome or not descricao or not categoria_id:
            erro = 'Nome, descrição e categoria são obrigatórios.'
        else:
            erro = validar_imagens_upload(imagens_novas)

            if not erro:
                imagens_restantes = produto.imagens.count() - len(imagens_deletar)
                total_imagens = imagens_restantes + len(imagens_novas)

                if total_imagens > 3:
                    erro = f'Limite de 3 imagens. Você terá {total_imagens} imagens no total, máximo permitido é 3.'
                else:
                    # Só remove as imagens depois que a validação do total passar
                    for img_id in imagens_deletar:
                        img = ProdutoImagem.objects.filter(id=img_id, produto=produto).first()
                        if img:
                            img.delete()

                    produto.nome = nome
                    produto.descricao = descricao
                    produto.tipo = tipo
                    produto.categoria = get_object_or_404(Categoria, id=categoria_id)
                    produto.destaque = destaque
                    produto.save()

                    for imagem in imagens_novas:
                        ProdutoImagem.objects.create(produto=produto, imagem=imagem)

                    return redirect('adm_produtos')

    return render(request, 'adm/produto_form.html', {
        'produto': produto,
        'categorias': categorias,
        'tipos': Produto.TIPOS,
        'erro': erro,
        'acao': 'Editar',
    })


@login_required(login_url='/adm/login/')
def adm_produto_deletar(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        # O delete() de cada ProdutoImagem já remove o arquivo físico
        for img in produto.imagens.all():
            img.delete()
        produto.delete()
        return redirect('adm_produtos')

    return render(request, 'adm/produto_confirmar_deletar.html', {'produto': produto})