from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # modelo python que será usado.
        model = User
        # campos que poderão ser serelizados ou desserializados
        fields = ["id","username","password"]
        #é uma forma de não retornar a senha na requisição
        extra_kwargs = {"password":{"write_only":True}}
        # é correto usar write_only, para que não devolva a senha

    def create(self,validated_data):
        # estou criando um novo usuário utilizando o modelo User.
        # devo usar o método create_user para que o campo password já seja criptografado
        # o **validated_data serve para converter os dados de um dicionário em argumentos da função.
        user = User.objects.create_user(**validated_data)
        # depois retornamos o usuário
        return user
    


class NoteSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Note

        field = ["id","title","content","created_at","author"]
        extra_kwargs ={"author":{"read_only":True}}

    
    