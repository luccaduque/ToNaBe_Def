from django.shortcuts import render, redirect
from django.db import models
from .models import Produto, Estoque, Venda
from django.utils.timezone import now
from django.db.models import Sum


def pagina_principal(request):
    return render(request, 'sistema/pagina_principal.html')


def pagina_estoque(request):
    return render(request, 'sistema/pagina_estoque.html')   


def pagina_vendas(request):
    return render(request, 'sistema/pagina_vendas.html')

def pagina_produtos(request):
    return render(request, 'sistema/pagina_produtos.html')


def adicionar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        detalhes = request.POST.get('detalhes')
        imagem = request.FILES.get('imagem')

        produto = Produto.objects.create(
            nome=nome,
            preco=preco,
            detalhes=detalhes,
            imagem=imagem
        )

        Estoque.objects.create(produto=produto, quantidade=0)
        return redirect('lista_produtos')
    return render(request, 'sistema/adicionar_produto.html')

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'sistema/lista_produtos.html', {'produtos': produtos})   


def alterar_estoque(request, id):
    estoque = Estoque.objects.get(produto_id=id)

    if request.method == 'POST':
        acao = request.POST['acao']   # ação -> adiciona ou remove
        quantidade = int(request.POST['quantidade'])

        if acao == "add":
            estoque.quantidade += quantidade
        elif acao == "remove":
            estoque.quantidade -= quantidade

        estoque.save()
        return redirect('lista_produtos')

    return render(request, 'alterar_estoque.html', {'estoque': estoque})

def registrar_venda(request, id):
    produto = Produto.objects.get(id=id)
    estoque = Estoque.objects.get(produto=produto)

    if request.method == 'POST':
        cliente = request.POST['cliente']
        quantidade = int(request.POST['quantidade'])

        # baixa estoque
        estoque.quantidade -= quantidade
        estoque.save()

        Venda.objects.create(
            produto=produto,
            cliente=cliente,
            quantidade=quantidade
        )

        return redirect('relatorio_vendas')

    return render(request, 'registrar_venda.html', {'produto': produto})


def relatorio_vendas(request):
    vendas = Venda.objects.all()
    
    faturamento = vendas.aggregate(
        total=Sum(models.F('quantidade') * models.F('produto__preco'))
    )['total'] or 0

    return render(request, 'relatorio_vendas.html', {
        'vendas': vendas,
        'faturamento': faturamento
    })

def faturamento_por_data(request):
    data_inicial = request.GET.get('inicio')
    data_final = request.GET.get('fim')

    vendas = Venda.objects.all()

    if data_inicial and data_final:
        vendas = vendas.filter(data__date__range=[data_inicial, data_final])

    faturamento = vendas.aggregate(
        total=Sum(models.F('quantidade') * models.F('produto__preco'))
    )['total'] or 0

    return render(request, 'faturamento_data.html', {
        'vendas': vendas,
        'faturamento': faturamento,
        'data_inicial': data_inicial,
        'data_final': data_final,
    })