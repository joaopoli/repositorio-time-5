import csv
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from SosAluno.professores.models import Instituicao, ComentarioInstituicao


class Command(BaseCommand):
    help = 'Importa instituições únicas de um arquivo CSV e adiciona comentários e avaliações fictícias'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Caminho para o arquivo CSV com os professores'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        comentarios_positivos = [
            "Ótima instituição com professores dedicados.",
            "Infraestrutura excelente para pesquisas.",
            "Ambiente acadêmico muito colaborativo.",
            "Ótimos laboratórios e infraestrutura.",
            "Corpo docente muito qualificado.",
        ]

        comentarios_negativos = [
            "Processo burocrático para matrícula.",
            "Falta de vagas em disciplinas importantes.",
            "Infraestrutura poderia ser melhor em alguns campi.",
            "Horários de atendimento pouco flexíveis.",
        ]

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                nomes = set()
                for row in reader:
                    nome = (row.get('Faculdade') or '').strip()
                    if nome and nome.lower() not in ('', 'não disponível', 'nao disponível'):
                        nomes.add(nome)

                created = 0
                for nome in sorted(nomes):
                    id_slug = slugify(nome)
                    if Instituicao.objects.filter(id_slug=id_slug).exists():
                        self.stdout.write(self.style.WARNING(f'Instituição {nome} já existe, pulando...'))
                        continue

                    avaliacao_geral = round(random.uniform(3.5, 5.0), 1)
                    total_avaliacoes = random.randint(10, 500)

                    instituicao = Instituicao.objects.create(
                        id_slug=id_slug,
                        nome=nome,
                        descricao=f'Instituição {nome} importada automaticamente a partir do CSV.',
                        localizacao='Não informada',
                        website='',
                        avaliacao_geral=avaliacao_geral,
                        total_avaliacoes=total_avaliacoes,
                    )

                    # Criar 1-3 comentários (pos/neg) para a instituição
                    num_comments = random.randint(1, 3)
                    for _ in range(num_comments):
                        tipo = 'positivo' if random.random() > 0.3 else 'negativo'
                        texto = random.choice(comentarios_positivos if tipo == 'positivo' else comentarios_negativos)
                        ComentarioInstituicao.objects.create(
                            instituicao=instituicao,
                            tipo=tipo,
                            texto=texto
                        )

                    self.stdout.write(self.style.SUCCESS(f'✓ Instituição "{nome}" criada. Avaliação: {avaliacao_geral} ({total_avaliacoes} avaliações)'))
                    created += 1

                self.stdout.write(self.style.SUCCESS(f'\n✓ Total de {created} instituições importadas.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar arquivo: {e}'))
