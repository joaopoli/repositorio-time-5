from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Professor, Comentario
from .serializers import ProfessorSerializer, ComentarioSerializer


def professores_list(request):
    """View para listar todos os professores (renderiza template HTML)."""
    professores = Professor.objects.all().prefetch_related('comentarios')
    context = {'professores': professores}
    return render(request, 'professores/professores_list.html', context)


def professor_detail(request, id_slug):
    """View para obter os detalhes de um professor específico (renderiza template HTML)."""
    professor = get_object_or_404(Professor, id_slug=id_slug)
    context = {'professor': professor}
    return render(request, 'professores/professor_detail.html', context)


def professores_list_api(request):
    """View para listar todos os professores em formato JSON (API)."""
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


def professor_detail_api(request, id_slug):
    """View para obter os detalhes de um professor específico em formato JSON (API)."""
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


def index(request):
    """View para a página inicial (index.html)."""
    return render(request, 'html/index.html')


# --- Views para Instituições ---

def instituicoes_list(request):
    """View para listar todas as instituições (renderiza template HTML)."""
    from .models import Instituicao
    instituicoes = Instituicao.objects.all().prefetch_related('cursos', 'comentarios')
    context = {'instituicoes': instituicoes}
    return render(request, 'instituicoes/instituicoes_list.html', context)


def instituicao_detail(request, id_slug):
    """View para obter os detalhes de uma instituição específica (renderiza template HTML)."""
    from .models import Instituicao
    instituicao = get_object_or_404(Instituicao, id_slug=id_slug)
    context = {'instituicao': instituicao}
    return render(request, 'instituicoes/instituicao_detail.html', context)


def curso_detail(request, id_slug):
    """View para obter os detalhes de um curso específico (renderiza template HTML)."""
    from .models import Curso
    curso = get_object_or_404(Curso, id_slug=id_slug)
    context = {'curso': curso}
    return render(request, 'instituicoes/curso_detail.html', context)

# --- Views para Autenticação ---

def login_view(request):
    """View para a página de login (login.html)."""
    return render(request, 'html/login.html')

def cadastro_view(request):
    """View para a página de cadastro (cadastro.html)."""
    return render(request, 'html/cadastro.html')
