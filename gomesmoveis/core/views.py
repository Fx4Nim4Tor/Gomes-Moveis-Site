from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Produto, Categoria, ProdutoImagem
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.cache import cache
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'}


def validar_imagens_upload(imagens):
    for imagem in imagens:
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


def inicio(request):
    from core.models import Categoria
    cats = [("Executiva","executiva"),("Secretária","secretaria"),("Presidente","presidente"),("Presidente Plus","presidente-plus"),("Back System","back-system"),("Gamer","gamer"),("Fixa","fixa"),("Plus Size","plus-size"),("Caixa","caixa"),("Mesas Retas","mesas-retas"),("Mesas em L","mesas-em-l"),("Mesas de Reunião","mesas-de-reuniao"),("Acessórios","acessorios"),("Diretor","diretor")]
    for nome, slug in cats:
        Categoria.objects.get_or_create(nome=nome, slug=slug)

    import time
    t1 = time.time()
    # Cache de 5 min — produtos destaque não mudam toda hora
    produtos_destaque = cache.get('produtos_destaque')
    if not produtos_destaque:
        produtos_destaque = list(
            Produto.objects
            .filter(destaque=True)
            .prefetch_related('imagens')   # FIX: template acessa produto.imagens.first — sem isso = N+1
            .select_related('categoria')
        )
        cache.set('produtos_destaque', produtos_destaque, 60 * 5)

    t2 = time.time()
    print(f"⏱️ Query levou: {t2-t1:.2f}s")

    return render(request, "index.html", {
        "produtos_destaque": produtos_destaque
    })


def produto(request, slug):
    produto = get_object_or_404(
        Produto.objects.prefetch_related('imagens').select_related('categoria'),
        slug=slug
    )

    # FIX: removido order_by("?") que fazia ORDER BY RANDOM() no banco
    # Agora pega só os IDs (query leve) e embaralha em Python
    ids = list(
        Produto.objects
        .filter(categoria=produto.categoria)
        .exclude(id=produto.id)
        .values_list('id', flat=True)[:20]
    )
    random.shuffle(ids)
    ids = ids[:4]

    produtos_relacionados = (
        Produto.objects
        .filter(id__in=ids)
        .prefetch_related('imagens')  # FIX: template acessa p.imagens.first — sem prefetch = N+1
    )

    return render(request, "produto.html", {
        "produto": produto,
        "produtos_relacionados": produtos_relacionados
    })


def produtos(request):
    # Cache de categorias — raramente mudam
    categorias = cache.get('categorias')
    if not categorias:
        categorias = list(Categoria.objects.all())
        cache.set('categorias', categorias, 60 * 10)

    tipo_produtos = Produto.TIPOS
    categorias_selecionadas = request.GET.getlist('categoria')
    tipos_selecionados = request.GET.getlist('tipo')
    page_number = request.GET.get('page', 1)
    sem_filtro = not categorias_selecionadas and not tipos_selecionados

    if sem_filtro:
        # FIX: removido CASE WHEN gigante que gerava SQL com centenas de WHENs
        # Agora pega só IDs (levíssimo), embaralha em Python, depois busca os dados paginados
        if str(page_number) == '1' or 'ordem_produtos' not in request.session:
            ids = list(Produto.objects.values_list('id', flat=True))
            random.shuffle(ids)
            request.session['ordem_produtos'] = ids

        ids_ordenados = request.session.get('ordem_produtos', [])

        # Paginação sobre a lista de IDs (sem tocar no banco ainda)
        paginator = Paginator(ids_ordenados, 12)
        pagina = paginator.get_page(page_number)
        ids_pagina = list(pagina.object_list)

        # Busca só os produtos da página atual com prefetch
        produtos_dict = {
            p.id: p for p in Produto.objects
            .filter(id__in=ids_pagina)
            .prefetch_related('imagens')
            .select_related('categoria')
        }
        # Preserva a ordem aleatória
        object_list_ordenado = [produtos_dict[i] for i in ids_pagina if i in produtos_dict]

        # Recria o objeto de página com os produtos ordenados
        pagina.object_list = object_list_ordenado
        itens = pagina

    else:
        qs = Produto.objects.prefetch_related('imagens').select_related('categoria')

        if categorias_selecionadas:
            qs = qs.filter(categoria__slug__in=categorias_selecionadas)
        if tipos_selecionados:
            qs = qs.filter(tipo__in=tipos_selecionados)

        paginator = Paginator(qs, 12)
        itens = paginator.get_page(page_number)

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
        # FIX: prefetch_related evita N+1 (antes chamava p.imagens.first() 2x por produto)
        produtos = (
            Produto.objects
            .filter(nome__icontains=query)
            .prefetch_related('imagens')[:6]
        )

        for p in produtos:
            imagens = p.imagens.all()
            resultados.append({
                'nome': p.nome,
                'slug': p.slug,
                'imagem': imagens[0].imagem.url if imagens else None,
            })

    return JsonResponse({'resultados': resultados})


def sobre(request):
    return render(request, "sobre.html")


# ADMIN TELAS
def adm_login(request):
    erro = None

    if request.user.is_authenticated:
        return redirect('adm_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('adm_dashboard')
        else:
            erro = 'Usuário ou senha inválidos.'

    return render(request, 'adm/login.html', {'erro': erro})


def adm_logout(request):
    logout(request)
    return redirect('adm_login')


@login_required(login_url='/adm/login/')
def adm_dashboard(request):
    return render(request, 'adm/dashboard.html')


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
            cache.delete('categorias')  # invalida cache
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
            cache.delete('categorias')  # invalida cache
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
            cache.delete('categorias')  # invalida cache
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
        cache.delete('categorias')  # invalida cache
        return redirect('adm_categorias')

    return render(request, 'adm/categoria_confirmar_deletar.html', {'categoria': categoria})


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

            cache.delete('produtos_destaque')  # invalida cache
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
        imagens_deletar = request.POST.getlist('deletar_imagem')

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

                    cache.delete('produtos_destaque')  # invalida cache
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
        for img in produto.imagens.all():
            img.delete()
        produto.delete()
        cache.delete('produtos_destaque')  # invalida cache
        return redirect('adm_produtos')

    return render(request, 'adm/produto_confirmar_deletar.html', {'produto': produto})