from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Professor, Comentario, Avaliacao
from .serializers import ProfessorSerializer, ComentarioSerializer
import json


def index(request):
    """View para servir a página index.html na raiz."""
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'index.html', context)


def professores_page(request):
    """View para servir a página professores.html."""
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'professores.html', context)


def professor_page(request, id_slug=None):
    """View para servir a página professor.html."""
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    if id_slug:
        try:
            professor = Professor.objects.get(id_slug=id_slug)
            context['professor'] = professor
        except Professor.DoesNotExist:
            pass
    return render(request, 'professor.html', context)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def login_page(request):
    """View para servir e processar login."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            senha = data.get('password')
            
            # Tenta encontrar o usuário pelo email ou username
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Email ou senha incorretos.'
                }, status=401)
            
            # Autentica com o username (já que o email pode não ser único)
            user = authenticate(request, username=user.username, password=senha)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login realizado com sucesso!',
                    'redirect': '/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Email ou senha incorretos.'
                }, status=401)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados inválidos.'
            }, status=400)
    
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'login.html', context)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def cadastro_page(request):
    """View para servir e processar cadastro."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome', '').strip()
            email = data.get('email', '').strip()
            senha = data.get('password', '').strip()
            confirmar_senha = data.get('confirm_password', '').strip()
            
            # Validações
            if not nome or not email or not senha or not confirmar_senha:
                return JsonResponse({
                    'success': False,
                    'message': 'Todos os campos são obrigatórios.'
                }, status=400)
            
            if senha != confirmar_senha:
                return JsonResponse({
                    'success': False,
                    'message': 'As senhas não coincidem.'
                }, status=400)
            
            if len(senha) < 6:
                return JsonResponse({
                    'success': False,
                    'message': 'A senha deve ter pelo menos 6 caracteres.'
                }, status=400)
            
            # Verifica se o email já existe
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este email já está cadastrado.'
                }, status=400)
            
            # Gera um username único a partir do email
            username = email.split('@')[0]
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Cria o novo usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=nome.split()[0] if nome else '',
                last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else ''
            )
            
            # Faz login automático
            login(request, user)
            
            return JsonResponse({
                'success': True,
                'message': 'Cadastro realizado com sucesso!',
                'redirect': '/'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados inválidos.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao cadastrar: {str(e)}'
            }, status=500)
    
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'cadastro.html', context)


def logout_user(request):
    """View para fazer logout."""
    logout(request)
    return redirect('/')


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


def avaliar_page(request):
    """View para servir a página de avaliação."""
    professores = Professor.objects.all()
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'professores': professores
    }
    return render(request, 'avaliar.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def salvar_avaliacao(request):
    """View para salvar uma avaliação de professor."""
    try:
        data = json.loads(request.body)
        professor_id = data.get('professor_id')
        nota = data.get('nota')
        comentario = data.get('comentario', '')

        # Validações
        if not professor_id or nota is None:
            return JsonResponse({
                'success': False,
                'message': 'Professor e nota são obrigatórios.'
            }, status=400)

        try:
            nota = float(nota)
            if nota < 0 or nota > 5:
                return JsonResponse({
                    'success': False,
                    'message': 'A nota deve estar entre 0 e 5.'
                }, status=400)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'message': 'Nota inválida.'
            }, status=400)

        try:
            professor = Professor.objects.get(id=professor_id)
        except Professor.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Professor não encontrado.'
            }, status=404)

        # Criar avaliação
        avaliacao = Avaliacao.objects.create(
            professor=professor,
            usuario=request.user if request.user.is_authenticated else None,
            nota=nota,
            comentario=comentario
        )

        # Atualizar avaliação geral do professor
        todas_avaliacoes = Avaliacao.objects.filter(professor=professor)
        media = todas_avaliacoes.aggregate(models.Avg('nota'))['nota__avg'] or 0
        professor.avaliacao_geral = round(media, 1)
        professor.total_avaliacoes = todas_avaliacoes.count()
        professor.save()

        return JsonResponse({
            'success': True,
            'message': 'Avaliação salva com sucesso!',
            'avaliacao_id': avaliacao.id
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao salvar avaliação: {str(e)}'
        }, status=500)
