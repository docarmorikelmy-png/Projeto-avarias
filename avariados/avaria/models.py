from django.db import models
from datetime import datetime

from django.db import models

class produto(models.Model):
    codigo_produto = models.CharField(max_length=14, unique=True)  # CharField evita perder zero à esquerda
    nome_produto = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo_produto} - {self.nome_produto}"


class avarias(models.Model):
    STATUS = [
        ("aberto", "Em aberto"),
        ("andamento", "Em andamento"),
        ("concluido", "Concluído"),
    ]

    colaborador = models.CharField(max_length=100)
    produto = models.ForeignKey(produto, on_delete=models.PROTECT)
    descricao_avaria = models.TextField()  # descrição de como o produto está avariado
    quantidade = models.DecimalField(max_digits=10, decimal_places=0)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default="aberto")
    concluido_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.colaborador} - {self.produto} - {self.quantidade}"

class Divergencia(models.Model):
    TIPOS = [
        ("positivo", "Positiva"),
        ("negativo", "Negativa"),
    ]
    STATUS = [
        ("aberto", "Em aberto"),
        ("andamento", "Em andamento"),
        ("concluido", "Concluído"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS)
    colaborador = models.CharField(max_length=100)
    produto = models.ForeignKey(produto, on_delete=models.PROTECT)
    local = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=10, decimal_places=0)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default="aberto")
    concluido_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto} - {self.local}"
   

# Create your models here.
