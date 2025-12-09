import csv
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from SosAluno.professores.models import Instituicao, Curso, ComentarioCurso


class Command(BaseCommand):
    help = 'Importa cursos do CSV para as instituições'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Caminho para o arquivo CSV com os professores'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        # Mapeamento de disciplinas para descrições
        descricoes_cursos = {
            'Ciência da Computação': 'Curso focado em algoritmos, sistemas computacionais, desenvolvimento de software e inteligência artificial.',
            'Ciências Biológicas': 'Curso que estuda organismos vivos, ecologia, genética e biologia molecular.',
            'Engenharia de Energia': 'Curso que aborda sistemas de energia, energias renováveis e eficiência energética.',
            'Instrumentação Óptica e Fotônica': 'Estudo de sistemas ópticos avançados, laser e aplicações fotônicas.',
            'Materiais Semicondutores': 'Curso focado em propriedades e aplicações de materiais semicondutores em eletrônica.',
            'Políticas Públicas': 'Análise de formulação, implementação e avaliação de políticas públicas.',
            'Relações Internacionais': 'Estudo de relações entre estados, diplomacia, cooperação internacional e geopolítica.',
            'Sociologia': 'Análise das estruturas sociais, comportamentos coletivos e dinâmicas da sociedade.',
        }

        # Mapeamento de disciplinas para áreas
        areas_cursos = {
            'Ciência da Computação': 'Ciências Exatas',
            'Ciências Biológicas': 'Ciências Biológicas',
            'Engenharia de Energia': 'Engenharia',
            'Instrumentação Óptica e Fotônica': 'Engenharia',
            'Materiais Semicondutores': 'Engenharia',
            'Políticas Públicas': 'Ciências Humanas',
            'Relações Internacionais': 'Ciências Humanas',
            'Sociologia': 'Ciências Humanas',
        }

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                cursos_criados = {}

                for row in reader:
                    nome_disciplina = (row.get('Materia') or '').strip()
                    nome_instituicao = (row.get('Faculdade') or '').strip()

                    if not nome_disciplina or nome_instituicao.lower() not in ('ufabc', 'ufmg'):
                        continue

                    if nome_disciplina in cursos_criados:
                        continue

                    # Encontrar a instituição
                    instituicao = Instituicao.objects.filter(nome__icontains=nome_instituicao).first()
                    if not instituicao:
                        self.stdout.write(self.style.WARNING(f'Instituição {nome_instituicao} não encontrada'))
                        continue

                    # Verificar se curso já existe
                    id_slug = slugify(nome_disciplina)
                    if Curso.objects.filter(id_slug=id_slug, instituicao=instituicao).exists():
                        self.stdout.write(self.style.WARNING(f'Curso {nome_disciplina} já existe em {instituicao.nome}'))
                        continue

                    # Criar curso
                    avaliacao = round(random.uniform(3.5, 5.0), 1)
                    total_aval = random.randint(10, 100)

                    curso = Curso.objects.create(
                        id_slug=id_slug,
                        nome=nome_disciplina,
                        descricao=descricoes_cursos.get(nome_disciplina, f'Curso de {nome_disciplina}.'),
                        duracao='4 anos',
                        area=areas_cursos.get(nome_disciplina, 'Geral'),
                        instituicao=instituicao,
                        avaliacao_geral=avaliacao,
                        total_avaliacoes=total_aval,
                    )

                    # Adicionar comentários
                    comentarios_pos = [
                        'Disciplina bem estruturada com excelentes materiais didáticos.',
                        'Professores dedicados e aulas muito interessantes.',
                        'Ótimo para desenvolver pensamento crítico.',
                        'Conteúdo relevante e aplicável na prática.',
                        'Muito bem coordenado e bem executado.',
                    ]

                    comentarios_neg = [
                        'Pode ser desafiador para iniciantes.',
                        'Volume de conteúdo às vezes é muito intenso.',
                        'Falta mais exercícios práticos.',
                    ]

                    for _ in range(random.randint(1, 2)):
                        ComentarioCurso.objects.create(
                            curso=curso,
                            tipo='positivo',
                            texto=random.choice(comentarios_pos)
                        )

                    if random.random() > 0.5:
                        ComentarioCurso.objects.create(
                            curso=curso,
                            tipo='negativo',
                            texto=random.choice(comentarios_neg)
                        )

                    cursos_criados[nome_disciplina] = True
                    self.stdout.write(self.style.SUCCESS(f'✓ Curso "{nome_disciplina}" em {instituicao.nome} criado'))

                self.stdout.write(self.style.SUCCESS(f'\n✓ Total de {len(cursos_criados)} cursos criados!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {e}'))
