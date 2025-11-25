from django.shortcuts import render



def pagina_principal(request):
    return render(request, 'sistema/pagina_principal.html')


def estoque(request):
    return render(request, 'sistema/estoque.html')   


def vendas(request):
    return render(request, 'sistema/vendas.html')

def produtos(request):
    return render(request, 'sistema/produtos.html')
