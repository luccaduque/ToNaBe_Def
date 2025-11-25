from django.urls import path
from . import views


app_name = 'sistema'


urlpatterns = [
    path('pagina_principal/', views.pagina_principal, name='pagina_principal'),
    path('pagina_estoque/', views.pagina_estoque, name='pagina_estoque'),
    path('pagina_vendas/', views.pagina_vendas, name='pagina_vendas'),
    path('pagina_produtos/', views.pagina_produtos, name='pagina_produtos'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/add/', views.adicionar_produto, name='adicionar_produto'),
    path('estoque/<int:id>/', views.alterar_estoque, name='alterar_estoque'),
    path('venda/<int:id>/', views.registrar_venda, name='registrar_venda'),
    path('vendas/', views.relatorio_vendas, name='relatorio_vendas'),
    path('faturamento/', views.faturamento_por_data, name='faturamento_por_data'),

]