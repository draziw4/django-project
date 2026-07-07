from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer,NoteSerialzer
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Note

class CreateUserView(generics.CreateAPIView):
    # faz uma pesquisa em todos os objetos de User para não criar algo que utilize os mesmos dados do banco de dados e não criar um usuário que já existe
    queryset = User.objects.all()
    # aqui diz para a view qual tipo de dado nos precisamos aceitar para fazer um novo usuário
    serializer_class = UserSerializer
    # especifica quem pode chamar isso  nesse caso nos podemos permitir qualquer um  até se ele não estiver autenticado para usar essa view de criar novo usuário
    permission_classes = [AllowAny]

# usamos o List pois será criado uma nota e irá mostrar a lista de notas criadas 
class NoteListCreate(generics.ListCreateAPIView):

    serializer_class=NoteSerialzer
     # só pode acessar essa site quem tem um JWT token
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
          # no django se eu quero pegar o usuário que está autenticado eu só prciso fazer isso dentro da nossa classe baseada em views
          user = self.request.user
          # e aqui estamos pegando todos os usuarios com um filtro que o author seja o mesmo user que está fazendo a requisiçao
          return Note.objects.filter(author = user)
     
    def perform_create(self,serializer):
        # caso eu queira alterar alguma coisa ele irá passar pela mesma classe que serializa, valida e depois salva todos os dados e envia novamente o author com o usuário que está autenticado
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    
    serializer_class = NoteSerialzer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
          # no django se eu quero pegar o usuário que está autenticado eu só prciso fazer isso dentro da nossa classe baseada em views
          user = self.request.user
          # e aqui estamos pegando todos os usuarios com um filtro que o author seja o mesmo user que está fazendo a requisiçao
          return Note.objects.filter(author = user)
    
    
        
          
