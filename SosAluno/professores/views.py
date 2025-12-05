from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Professor, Comentario
from .serializers import ProfessorSerializer, ComentarioSerializer


def professores_list(request):
    """View para listar todos os professores em formato JSON."""
    professores = Professor.objects.all().prefetch_related('comentarios')
    data = []
    
    for prof in professores:
        prof_data = {
            'id': prof.id_slug,
            'nome': prof.nome,
            'foto': prof.foto.url if prof.foto else '/img/prof_default.jpg',
            'instituicao': prof.instituicao,
            'materia': prof.materia,
            'avaliacao_geral': prof.avaliacao_geral,
            'total_avaliacoes': prof.total_avaliacoes,
            'comentarios': [
                {
                    'tipo': c.tipo,
                    'texto': c.texto
                }
                for c in prof.comentarios.all()
            ]
        }
        data.append(prof_data)
    
    return JsonResponse(data, safe=False)


def professor_detail(request, id_slug):
    """View para obter os detalhes de um professor específico em formato JSON."""
    professor = get_object_or_404(Professor, id_slug=id_slug)
    
    data = {
        'id': professor.id_slug,
        'nome': professor.nome,
        'foto': professor.foto.url if professor.foto else '/img/prof_default.jpg',
        'instituicao': professor.instituicao,
        'materia': professor.materia,
        'avaliacao_geral': professor.avaliacao_geral,
        'total_avaliacoes': professor.total_avaliacoes,
        'comentarios': [
            {
                'tipo': c.tipo,
                'texto': c.texto
            }
            for c in professor.comentarios.all()
        ]
    }
    
    return JsonResponse(data)


class ProfessorViewSet(viewsets.ModelViewSet):
    """ViewSet para o modelo Professor (API REST)."""
    queryset = Professor.objects.all().prefetch_related('comentarios')
    serializer_class = ProfessorSerializer
    lookup_field = 'id_slug'


class ComentarioViewSet(viewsets.ModelViewSet):
    """ViewSet para o modelo Comentario (API REST)."""
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
