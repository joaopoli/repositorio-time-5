from django.shortcuts import render, get_object_or_404
from .models import Professor, Instituicao, Curso

# --- Views para Professores ---

def professores_list(request):
    """View para a página de listagem de professores (professores_list.html)."""
    professores = Professor.objects.all()
    return render(request, 'professores/professores_list.html', {'professores': professores})

def professor_detail(request, id_slug):
    """View para a página de detalhes de um professor (professor_detail.html)."""
    professor = get_object_or_404(Professor, id_slug=id_slug)
    return render(request, 'professores/professor_detail.html', {'professor': professor})

# --- Views para Instituições ---

def instituicoes_list(request):
    """View para a página de listagem de instituições (instituicoes_list.html)."""
    instituicoes = Instituicao.objects.all()
    return render(request, 'instituicoes/instituicoes_list.html', {'instituicoes': instituicoes})

def instituicao_detail(request, id_slug):
    """View para a página de detalhes de uma instituição (instituicao_detail.html)."""
    instituicao = get_object_or_404(Instituicao, id_slug=id_slug)
    return render(request, 'instituicoes/instituicao_detail.html', {'instituicao': instituicao})

# --- Views para Cursos ---

def curso_detail(request, id_slug):
    """View para a página de detalhes de um curso (curso_detail.html)."""
    curso = get_object_or_404(Curso, id_slug=id_slug)
    return render(request, 'instituicoes/curso_detail.html', {'curso': curso})

# --- Views para Páginas Estáticas ---

def index(request):
    """View para a página inicial (index.html)."""
    return render(request, 'index.html')

def sobre(request):
    """View para a página Sobre."""
    return render(request, 'sobre.html')

def contato(request):
    """View para a página Contato."""
    return render(request, 'contato.html')

def privacidade(request):
    """View para a página Política de Privacidade."""
    return render(request, 'privacidade.html')

def termos(request):
    """View para a página Termos de Uso."""
    return render(request, 'termos.html')

# --- Views para Autenticação ---

from rest_framework import viewsets
from .models import Professor, Comentario
from .serializers import ProfessorSerializer, ComentarioSerializer

# --- ViewSets para API REST ---

class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

from django.http import JsonResponse
from .serializers import ProfessorSerializer

# --- Views para JSON simples (API) ---

def professores_list_api(request):
    """API para listagem de professores em JSON."""
    professores = Professor.objects.all()
    serializer = ProfessorSerializer(professores, many=True)
    return JsonResponse(serializer.data, safe=False)

def professor_detail_api(request, id_slug):
    """API para detalhes de um professor em JSON."""
    professor = get_object_or_404(Professor, id_slug=id_slug)
    serializer = ProfessorSerializer(professor)
    return JsonResponse(serializer.data)
