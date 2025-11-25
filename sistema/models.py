from django.db import models


class Produto(models.Model):
    """Produtos Cadastrados"""
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Devolve uma representação em string do modelo"""
        return self.nome
    

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} — {self.quantidade}"


class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=1)
    data = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.quantidade * self.produto.preco

    def __str__(self):
        return f"Venda de {self.produto.nome}"