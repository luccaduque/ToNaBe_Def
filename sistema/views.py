from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Produto, Estoque, Venda
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Sum, F



def pagina_principal(request):
    total_faturamento = Venda.objects.aggregate(
        total=Sum(models.F('quantidade') * models.F('produto__preco'))
    )['total'] or 0

    estoques = Estoque.objects.select_related('produto').all()

    return render(request, 'sistema/pagina_principal.html', {
        'total_faturamento': total_faturamento,
        'estoques': estoques
    })


def pagina_produtos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        imagem = request.FILES.get('imagem')

        produto = Produto.objects.create(
            nome=nome,
            preco=preco,
            imagem=imagem
        )

        Estoque.objects.create(produto=produto, quantidade=0)

    
    produtos = Produto.objects.all()
    
    return render(request, 'sistema/pagina_produtos.html', {
        'produtos': produtos
    })



def pagina_estoque(request):

    produtos = Produto.objects.all()
    estoques = Estoque.objects.select_related('produto').all()

    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        acao = request.POST.get('acao')
        quantidade = int(request.POST.get('quantidade'))

        estoque = Estoque.objects.get(produto_id=produto_id)

        if acao == 'add':
            estoque.quantidade += quantidade
        else:
            estoque.quantidade -= quantidade

        estoque.save()

    return render(request, 'sistema/pagina_estoque.html', {
        'produtos': produtos,
        'estoques': estoques
    })
  


def pagina_vendas(request):

    produtos = Produto.objects.all()
    vendas = Venda.objects.select_related('produto').all()

    if request.method == "POST":
        produto_id = request.POST.get('produto_id')
        cliente = request.POST.get('cliente')
        quantidade = int(request.POST.get('quantidade'))

        produto = Produto.objects.get(id=produto_id)
        estoque = Estoque.objects.get(produto=produto)

        if estoque.quantidade >= quantidade:
            estoque.quantidade -= quantidade
            estoque.save()

            Venda.objects.create(
                produto=produto,
                cliente=cliente,
                quantidade=quantidade
            )

    return render(request, 'sistema/pagina_vendas.html', {
        'produtos': produtos,
        'vendas': vendas
    })


def atualizar_estoque(request, produto_id, acao):
    produto = get_object_or_404(Produto, id=produto_id)

    # Garante que o produto tem um registro de estoque
    estoque, created = Estoque.objects.get_or_create(produto=produto)

    if acao == "add":
        estoque.quantidade += 1

    elif acao == "remove":
        if estoque.quantidade > 0:
            estoque.quantidade -= 1

    estoque.save()

    return redirect('sistema:pagina_estoque')


def registrar_venda(request):
    if request.method == "POST":
        produto_id = request.POST.get("produto")
        cliente = request.POST.get("cliente")
        quantidade = int(request.POST.get("quantidade"))

        produto = get_object_or_404(Produto, id=produto_id)
        estoque, created = Estoque.objects.get_or_create(produto=produto)

        # Verifica estoque disponível
        if estoque.quantidade < quantidade:
            messages.error(request, "Estoque insuficiente para realizar a venda.")
            return redirect("sistema:pagina_vendas")

        # Registrar venda
        venda = Venda.objects.create(
            produto=produto,
            cliente=cliente,
            quantidade=quantidade
        )

        # Atualizar estoque
        estoque.quantidade -= quantidade
        estoque.save()

        messages.success(request, "Venda registrada com sucesso!")
        return redirect("sistema:pagina_vendas")

    return redirect("sistema:pagina_vendas")