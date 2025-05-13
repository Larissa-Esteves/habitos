from django.db import models
from django.contrib.auth.models import User

class Habito(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Relaciona cada hábito a um usuário. Se o usuário for deletado, seus hábitos também serão deletados.

    def __str__(self):
        return self.nome
