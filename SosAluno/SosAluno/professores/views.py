from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
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

def avaliar_professor(request, id_slug):
    """View para avaliação de um professor (página com formulário de nota + comentário)."""
    professor = get_object_or_404(Professor, id_slug=id_slug)
    error = None
    
    if request.method == 'POST':
        nota = request.POST.get('nota', '').strip()
        comentario = request.POST.get('comentario', '').strip()
        
        # Validação
        if not nota or not comentario:
            error = 'Por favor, preencha a nota e o comentário.'
        elif not nota.isdigit() or int(nota) < 1 or int(nota) > 5:
            error = 'A nota deve ser um número entre 1 e 5.'
        elif len(comentario) < 10:
            error = 'O comentário deve ter pelo menos 10 caracteres.'
        else:
            # Determinar tipo baseado na nota
            tipo = 'positivo' if int(nota) >= 3 else 'negativo'
            
            # Criar comentário
            novo_comentario = Comentario.objects.create(
                professor=professor,
                nota=int(nota),
                tipo=tipo,
                texto=comentario
            )
            
            # Atualizar avaliação geral do professor
            comentarios = professor.comentarios.all()
            total_notas = sum([c.nota for c in comentarios])
            total_avaliacoes = comentarios.count()
            
            professor.avaliacao_geral = total_notas / total_avaliacoes if total_avaliacoes > 0 else 0
            professor.total_avaliacoes = total_avaliacoes
            professor.save()
            
            # Redirecionar para a página do professor
            return redirect('professor-detail', id_slug=id_slug)
    
    return render(request, 'professores/professor_avaliar.html', {
        'professor': professor,
        'error': error,
        'is_authenticated': request.user.is_authenticated,
        'user': request.user
    })

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
    return render(request, 'index.html', {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user
    })

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


def login_view(request):
    """Renderiza a página de login e responde a POST com um JSON (simples).
    A função de autenticação completa não está implementada — retorna JSON informando isso.
    """
    error = None
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '').strip()

        user = None
        # Tentar autenticar por username
        user = authenticate(request, username=identifier, password=password)
        if not user:
            # Tentar por email
            try:
                u = User.objects.filter(email__iexact=identifier).first()
                if u:
                    user = authenticate(request, username=u.username, password=password)
            except Exception:
                user = None

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = 'Usuário ou senha inválidos.'

    return render(request, 'login.html', {'error': error})


def cadastro_view(request):
    """Renderiza a página de cadastro e responde a POST com um JSON (simples).
    A funcionalidade real de criação de usuário não está implementada aqui.
    """
    error = None
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not fullname or not email or not password:
            error = 'Todos os campos são obrigatórios.'
        elif password != confirm_password:
            error = 'As senhas não coincidem.'
        elif User.objects.filter(email__iexact=email).exists():
            error = 'Já existe uma conta com esse e-mail.'
        else:
            username_base = email.split('@')[0]
            username = username_base
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{username_base}{counter}"
                counter += 1

            user = User.objects.create_user(username=username, email=email, password=password, first_name=fullname)
            login(request, user)
            return redirect('index')

    return render(request, 'cadastro.html', {'error': error})

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
