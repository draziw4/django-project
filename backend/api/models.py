from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Note(models.Model):
    # aqui criamos os campos que serão correspondentes as colunas da nossa tabela do banco de dados NOTE
    title = models.CharField(max_length=100)
    content = models.TextField()
    # automaticamente ele cria
    created_at = models.DateTimeField(auto_now_add=True)

    # Essa chave está dizendo que está relacionada ao USER, quando for deletada deletará todas em cascada e tem uma linha relacionada com ela lá no modelo USER
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notes")

    def __str__(self):
        return self.title

