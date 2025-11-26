from django.urls import path
from . import views


app_name = 'sistema'


urlpatterns = [
    path('pagina_principal/', views.pagina_principal, name='pagina_principal'),
    path('pagina_estoque/', views.pagina_estoque, name='pagina_estoque'),
    path('pagina_vendas/', views.pagina_vendas, name='pagina_vendas'),
    path('pagina_produtos/', views.pagina_produtos, name='pagina_produtos'),
    path('produtos/', views.pagina_produtos, name='lista_produtos'),
    path('estoque/', views.pagina_estoque, name='pagina_estoque'),
    path('estoque/atualizar/<int:produto_id>/<str:acao>/', views.atualizar_estoque, name='atualizar_estoque'),
    path('vendas/', views.pagina_vendas, name='pagina_vendas'),
    path('vendas/registrar/', views.registrar_venda, name='registrar_venda'),
    


]