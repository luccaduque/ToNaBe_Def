from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'sistema'


urlpatterns = [
    path('pagina_principal/', views.pagina_principal, name='pagina_principal'),
    path('estoque/', views.estoque, name='estoque'),
    path('vendas/', views.vendas, name='vendas'),
    path('produtos/', views.produtos, name='produtos'),
]