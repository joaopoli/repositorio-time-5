from rest_framework import serializers
from .models import Professor, Comentario


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Comentario."""
    class Meta:
        model = Comentario
        fields = ['id', 'professor', 'tipo', 'texto', 'criado_em']
        read_only_fields = ['id', 'criado_em']


class ProfessorSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Professor."""
    comentarios = ComentarioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Professor
        fields = ['id', 'id_slug', 'nome', 'foto', 'instituicao', 'materia', 
                  'avaliacao_geral', 'total_avaliacoes', 'comentarios', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
