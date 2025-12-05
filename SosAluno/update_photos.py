#!/usr/bin/env python
"""
Script para atualizar as fotos dos professores na base de dados.
"""
import os
import sys
import django

# Configurar o Django
sys.path.append('/home/ubuntu/ENG4021-1/SosAluno')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SosAluno.settings')
django.setup()

from SosAluno.professores.models import Professor

# Mapeamento de professores para fotos
fotos_map = {
    'alexandre-meslin': 'professores/prof_alexandre.jpg',
    'ana-silva': 'professores/prof_ana.jpg',
    'carlos-rodrigues': 'professores/prof_carlos.jpg',
}

# Atualizar as fotos
for id_slug, foto_path in fotos_map.items():
    try:
        professor = Professor.objects.get(id_slug=id_slug)
        professor.foto = foto_path
        professor.save()
        print(f"✓ Foto atualizada para {professor.nome}: {foto_path}")
    except Professor.DoesNotExist:
        print(f"✗ Professor com id_slug '{id_slug}' não encontrado.")
    except Exception as e:
        print(f"✗ Erro ao atualizar {id_slug}: {e}")

print("\nAtualização concluída!")
