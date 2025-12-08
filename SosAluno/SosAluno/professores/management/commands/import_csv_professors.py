import csv
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from SosAluno.professores.models import Professor, Comentario


class Command(BaseCommand):
    help = 'Importa professores de um arquivo CSV e adiciona avaliações e comentários'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Caminho para o arquivo CSV com os professores'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        # Dados fictícios para comentários
        comentarios_positivos = [
            "Excelente professor! Muito dedicado ao ensino.",
            "As aulas são muito claras e bem estruturadas.",
            "Professsor super atencioso com os alunos.",
            "Conteúdo apresentado de forma muito didática.",
            "Recomendo muito! Aprendi bastante.",
            "Aulas inspiradoras e motivadoras.",
            "Domina muito bem o assunto.",
            "Muito paciente na hora de tirar dúvidas.",
            "Matéria complexa explicada com simplicidade.",
            "Professor nota 10!",
            "Suas listas de exercícios ajudaram muito.",
            "Feedback detalhado nas provas.",
            "Cria um ótimo ambiente para aprender.",
            "Prova coerente com o que foi ensinado.",
            "Professor que realmente se importa com seus alunos.",
        ]
        
        comentarios_negativos = [
            "Aulas um pouco monótonas.",
            "Matéria é complexa, poderia explicar melhor.",
            "Provas muito difíceis em relação ao que foi ensinado.",
            "Pouco tempo de atendimento aos alunos.",
            "Material de estudo poderia ser mais organizado.",
            "Ritmo das aulas um pouco acelerado.",
            "Poderia fornecer mais exemplos práticos.",
            "Avaliação muito rigorosa.",
            "Aulas faltam casos reais de aplicação.",
            "Deveria dedicar mais tempo a revisão.",
        ]
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                professores_criados = 0
                
                for row in reader:
                    nome = row.get('Nome', '').strip()
                    materia = row.get('Materia', '').strip()
                    instituicao = row.get('Faculdade', '').strip()
                    
                    if not nome or not materia or not instituicao:
                        continue
                    
                    # Criar slug único
                    id_slug = slugify(nome)
                    
                    # Verificar se professor já existe
                    if Professor.objects.filter(id_slug=id_slug).exists():
                        self.stdout.write(f"Professor {nome} já existe, pulando...")
                        continue
                    
                    # Gerar avaliação aleatória entre 3.5 e 5.0
                    avaliacao_geral = round(random.uniform(3.5, 5.0), 1)
                    
                    # Gerar número de avaliações aleatório entre 15 e 150
                    total_avaliacoes = random.randint(15, 150)
                    
                    # Criar professor
                    professor = Professor.objects.create(
                        id_slug=id_slug,
                        nome=nome,
                        materia=materia,
                        instituicao=instituicao,
                        avaliacao_geral=avaliacao_geral,
                        total_avaliacoes=total_avaliacoes,
                    )
                    
                    # Adicionar 2-4 comentários positivos
                    num_positivos = random.randint(2, 4)
                    for _ in range(num_positivos):
                        Comentario.objects.create(
                            professor=professor,
                            tipo='positivo',
                            texto=random.choice(comentarios_positivos)
                        )
                    
                    # Adicionar 0-2 comentários negativos
                    num_negativos = random.randint(0, 2)
                    for _ in range(num_negativos):
                        Comentario.objects.create(
                            professor=professor,
                            tipo='negativo',
                            texto=random.choice(comentarios_negativos)
                        )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Professor "{nome}" criado com sucesso. '
                            f'Avaliação: {avaliacao_geral}/5.0 ({total_avaliacoes} avaliações)'
                        )
                    )
                    professores_criados += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ Total de {professores_criados} professores importados com sucesso!'
                    )
                )
        
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Arquivo não encontrado: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao processar arquivo: {str(e)}')
            )
