from django.contrib import admin
from django.urls import path, include
from core.views import produto ,inicio, produtos,buscar,adm_dashboard,adm_login,adm_logout,adm_categoria_criar,adm_categoria_deletar,adm_categoria_editar,adm_categorias,adm_produtos_criar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('buscar/',buscar, name='buscar'),
    path("produtos/",produtos, name="produtos"),
    path("produtos/<slug:slug>/",produto, name="produto"),
    path("admin/",admin.site.urls),
    path("", inicio,name="inicio"),

    # Rela de adm
    path("adm/login/", adm_login, name="adm_login"),
    path("adm/logout/", adm_logout, name="adm_logout"),
    path("adm/", adm_dashboard, name="adm_dashboard"),

    # Categorias
    path("adm/categorias/", adm_categorias, name="adm_categorias"),
    path("adm/categorias/editar/<int:id>/", adm_categoria_editar, name="adm_categoria_editar"),
    path("adm/categorias/deletar/<int:id>/", adm_categoria_deletar, name="adm_categoria_deletar"),

    # Produtos
    path("adm/produtos/",adm_produtos_criar, name="adm_produtos_criar"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)