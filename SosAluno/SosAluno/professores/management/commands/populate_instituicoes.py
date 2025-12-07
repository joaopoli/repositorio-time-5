from django.core.management.base import BaseCommand
from SosAluno.professores.models import Instituicao, ComentarioInstituicao, Curso, ComentarioCurso


class Command(BaseCommand):
    help = 'Popula a base de dados com instituições e cursos simulados'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populando a base de dados com instituições e cursos...')

        # Limpar dados existentes
        Instituicao.objects.all().delete()
        
        # Criar PUC-Rio
        puc = Instituicao.objects.create(
            id_slug='puc-rio',
            nome='PUC-Rio',
            descricao='Pontifícia Universidade Católica do Rio de Janeiro - Uma das melhores universidades privadas do Brasil.',
            localizacao='Rio de Janeiro, RJ',
            website='https://www.puc-rio.br',
            avaliacao_geral=4.7,
            total_avaliacoes=150
        )
        
        ComentarioInstituicao.objects.create(
            instituicao=puc,
            tipo='positivo',
            texto='Excelente infraestrutura e corpo docente qualificado!'
        )
        
        ComentarioInstituicao.objects.create(
            instituicao=puc,
            tipo='negativo',
            texto='Mensalidade muito alta para alguns cursos.'
        )
        
        # Cursos da PUC-Rio
        Curso.objects.create(
            id_slug='engenharia-software-puc',
            nome='Engenharia de Software',
            descricao='Curso focado em desenvolvimento de sistemas e gestão de projetos de software.',
            duracao='5 anos',
            area='Engenharia',
            instituicao=puc,
            avaliacao_geral=4.8,
            total_avaliacoes=80
        )
        
        Curso.objects.create(
            id_slug='ciencia-computacao-puc',
            nome='Ciência da Computação',
            descricao='Curso com foco em algoritmos, inteligência artificial e computação teórica.',
            duracao='4 anos',
            area='Ciências Exatas',
            instituicao=puc,
            avaliacao_geral=4.6,
            total_avaliacoes=95
        )
        
        # Criar UFRJ
        ufrj = Instituicao.objects.create(
            id_slug='ufrj',
            nome='UFRJ',
            descricao='Universidade Federal do Rio de Janeiro - A maior universidade federal do Brasil.',
            localizacao='Rio de Janeiro, RJ',
            website='https://www.ufrj.br',
            avaliacao_geral=4.5,
            total_avaliacoes=200
        )
        
        ComentarioInstituicao.objects.create(
            instituicao=ufrj,
            tipo='positivo',
            texto='Universidade pública de excelência com ótimos professores!'
        )
        
        ComentarioInstituicao.objects.create(
            instituicao=ufrj,
            tipo='negativo',
            texto='Infraestrutura precisa de melhorias em alguns prédios.'
        )
        
        # Cursos da UFRJ
        Curso.objects.create(
            id_slug='matematica-ufrj',
            nome='Matemática',
            descricao='Curso de licenciatura e bacharelado em matemática pura e aplicada.',
            duracao='4 anos',
            area='Ciências Exatas',
            instituicao=ufrj,
            avaliacao_geral=4.4,
            total_avaliacoes=60
        )
        
        Curso.objects.create(
            id_slug='fisica-ufrj',
            nome='Física',
            descricao='Curso com foco em física experimental e teórica.',
            duracao='4 anos',
            area='Ciências Exatas',
            instituicao=ufrj,
            avaliacao_geral=4.3,
            total_avaliacoes=55
        )
        
        # Criar USP
        usp = Instituicao.objects.create(
            id_slug='usp',
            nome='USP',
            descricao='Universidade de São Paulo - A melhor universidade da América Latina.',
            localizacao='São Paulo, SP',
            website='https://www.usp.br',
            avaliacao_geral=4.9,
            total_avaliacoes=300
        )
        
        ComentarioInstituicao.objects.create(
            instituicao=usp,
            tipo='positivo',
            texto='Referência em pesquisa e ensino de qualidade!'
        )
        
        ComentarioInstituicao.objects.create(
            instituicao=usp,
            tipo='negativo',
            texto='Processo seletivo muito concorrido.'
        )
        
        # Cursos da USP
        Curso.objects.create(
            id_slug='engenharia-eletrica-usp',
            nome='Engenharia Elétrica',
            descricao='Curso com foco em sistemas elétricos, eletrônica e telecomunicações.',
            duracao='5 anos',
            area='Engenharia',
            instituicao=usp,
            avaliacao_geral=4.9,
            total_avaliacoes=120
        )
        
        Curso.objects.create(
            id_slug='medicina-usp',
            nome='Medicina',
            descricao='Um dos melhores cursos de medicina do Brasil.',
            duracao='6 anos',
            area='Ciências da Saúde',
            instituicao=usp,
            avaliacao_geral=5.0,
            total_avaliacoes=150
        )
        
        self.stdout.write(self.style.SUCCESS('Base de dados populada com sucesso!'))
        self.stdout.write(f'✓ Criadas 3 instituições')
        self.stdout.write(f'✓ Criados 6 cursos')
        self.stdout.write(f'✓ Criados 6 comentários de instituições')
