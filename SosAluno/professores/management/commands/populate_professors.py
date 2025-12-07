from django.core.management.base import BaseCommand
from django.utils.text import slugify
from professores.models import Professor, Comentario
import csv
import random
from pathlib import Path


class Command(BaseCommand):
    help = 'Popula a base de dados com professores a partir do arquivo CSV'

    def handle(self, *args, **options):
        # Caminho para o arquivo CSV
        csv_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'ENG4021' / 'professores_20.csv'
        
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f'Arquivo CSV não encontrado em {csv_path}'))
            return
        
        # Comentários de exemplo para adicionar aos professores
        comentarios_positivos = [
            'Excelente professor! As aulas são muito claras e didáticas.',
            'Muito dedicado e preocupado com o aprendizado dos alunos.',
            'As avaliações são justas e o feedback é construtivo.',
            'Aulas dinâmicas e envolventes. Recomendo muito!',
            'Professor com amplo conhecimento e muito acessível.',
            'Material de aula bem preparado e de fácil compreensão.',
            'Muito paciente em esclarecer dúvidas.',
            'Excelente didática! Melhor professor que já tive.',
        ]
        
        comentarios_negativos = [
            'Poderia melhorar a estrutura das aulas.',
            'Às vezes falta clareza nos explicações.',
            'Avaliações muito rigorosas.',
            'Pouco acessível fora do horário de aula.',
            'Ritmo das aulas é um pouco acelerado.',
            'Falta mais interação em sala de aula.',
        ]
        
        # Limpar dados existentes (opcional)
        Professor.objects.all().delete()
        self.stdout.write(self.style.WARNING('Professores existentes foram deletados.'))
        
        professores_criados = 0
        
        # Ler e processar o arquivo CSV
        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    nome = row['Nome'].strip()
                    materia = row['Materia'].strip()
                    instituicao = row['Faculdade'].strip()
                    
                    # Gerar ID slug a partir do nome
                    id_slug = slugify(nome)
                    
                    # Gerar valores demonstrativos
                    avaliacao_geral = round(random.uniform(2.5, 5.0), 1)
                    total_avaliacoes = random.randint(15, 150)
                    
                    # Criar ou atualizar professor
                    professor, created = Professor.objects.get_or_create(
                        id_slug=id_slug,
                        defaults={
                            'nome': nome,
                            'materia': materia,
                            'instituicao': instituicao,
                            'avaliacao_geral': avaliacao_geral,
                            'total_avaliacoes': total_avaliacoes,
                        }
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Professor "{nome}" ({instituicao}) - '
                                f'Avaliação: {avaliacao_geral}/5.0 ({total_avaliacoes} avaliações)'
                            )
                        )
                        
                        # Adicionar alguns comentários aleatórios
                        num_comentarios = random.randint(2, 5)
                        comentarios_usados = set()  # Rastrear comentários já usados
                        
                        for _ in range(num_comentarios):
                            is_positivo = random.random() > 0.3  # 70% de chance de ser positivo
                            tipo = 'positivo' if is_positivo else 'negativo'
                            comentarios = comentarios_positivos if is_positivo else comentarios_negativos
                            
                            # Selecionar um comentário que ainda não foi usado
                            comentario_texto = random.choice(comentarios)
                            tentativas = 0
                            while comentario_texto in comentarios_usados and tentativas < 10:
                                comentario_texto = random.choice(comentarios)
                                tentativas += 1
                            
                            # Se encontrou um comentário único, adicionar
                            if comentario_texto not in comentarios_usados:
                                comentarios_usados.add(comentario_texto)
                                Comentario.objects.create(
                                    professor=professor,
                                    tipo=tipo,
                                    texto=comentario_texto
                                )
                        
                        professores_criados += 1
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'⚠ Professor "{nome}" já existia.')
                        )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Sucesso! {professores_criados} professores foram criados/atualizados.'
                )
            )
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar CSV: {str(e)}'))


        self.stdout.write(self.style.SUCCESS('\n✓ Base de dados populada com sucesso!'))
