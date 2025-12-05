from django.core.management.base import BaseCommand
from professores.models import Professor, Comentario


class Command(BaseCommand):
    help = 'Popula a base de dados com professores simulados'

    def handle(self, *args, **options):
        # Dados dos professores
        professores_data = [
            {
                'id_slug': 'alexandre-meslin',
                'nome': 'Alexandre Meslin',
                'instituicao': 'PUC-Rio',
                'materia': 'Projeto de Software',
                'avaliacao_geral': 4.8,
                'total_avaliacoes': 95,
                'comentarios': [
                    {
                        'tipo': 'positivo',
                        'texto': 'Melhor professor de Projeto de Software! As aulas são super práticas e ele realmente se importa com o aprendizado dos alunos.'
                    },
                    {
                        'tipo': 'positivo',
                        'texto': 'O Meslin é um mestre em simplificar conceitos complexos. O projeto final foi desafiador, mas muito gratificante.'
                    },
                    {
                        'tipo': 'negativo',
                        'texto': 'A matéria é ótima, mas a correção das provas é um pouco rigorosa demais. Às vezes, sinto falta de um feedback mais detalhado.'
                    }
                ]
            },
            {
                'id_slug': 'ana-silva',
                'nome': 'Ana Silva',
                'instituicao': 'UFRJ',
                'materia': 'Cálculo I',
                'avaliacao_geral': 3.5,
                'total_avaliacoes': 120,
                'comentarios': [
                    {
                        'tipo': 'positivo',
                        'texto': 'Explica muito bem a teoria. As listas de exercícios ajudam bastante a fixar o conteúdo.'
                    },
                    {
                        'tipo': 'negativo',
                        'texto': 'As aulas são um pouco monótonas e a professora não é muito acessível fora do horário de aula.'
                    }
                ]
            },
            {
                'id_slug': 'carlos-rodrigues',
                'nome': 'Carlos Rodrigues',
                'instituicao': 'USP',
                'materia': 'Física Moderna',
                'avaliacao_geral': 4.1,
                'total_avaliacoes': 78,
                'comentarios': [
                    {
                        'tipo': 'positivo',
                        'texto': 'Muito didático e apaixonado pelo que ensina. As demonstrações em aula são incríveis.'
                    },
                    {
                        'tipo': 'negativo',
                        'texto': 'O ritmo é muito acelerado. Quem não tem base em física sofre um pouco para acompanhar.'
                    }
                ]
            }
        ]

        # Limpar dados existentes (opcional)
        Professor.objects.all().delete()
        self.stdout.write(self.style.WARNING('Professores existentes foram deletados.'))

        # Criar professores e seus comentários
        for prof_data in professores_data:
            comentarios_data = prof_data.pop('comentarios')
            
            # Criar professor
            professor, created = Professor.objects.get_or_create(
                id_slug=prof_data['id_slug'],
                defaults=prof_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Professor "{professor.nome}" criado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Professor "{professor.nome}" já existia.'))
            
            # Criar comentários
            for comentario_data in comentarios_data:
                comentario, created = Comentario.objects.get_or_create(
                    professor=professor,
                    tipo=comentario_data['tipo'],
                    texto=comentario_data['texto']
                )
                
                if created:
                    self.stdout.write(f'  └─ Comentário {comentario_data["tipo"]} adicionado.')

        self.stdout.write(self.style.SUCCESS('\n✓ Base de dados populada com sucesso!'))
