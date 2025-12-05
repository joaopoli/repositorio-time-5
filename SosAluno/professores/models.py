from django.db import models

class Professor(models.Model):
    """Modelo para armazenar informações dos professores."""
    id_slug = models.SlugField(unique=True, max_length=100, help_text="ID único do professor (ex: alexandre-meslin)")
    nome = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='professores/', null=True, blank=True)
    instituicao = models.CharField(max_length=200)
    materia = models.CharField(max_length=200)
    avaliacao_geral = models.FloatField(default=0.0, help_text="Avaliação de 0 a 5")
    total_avaliacoes = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-avaliacao_geral']
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome


class Comentario(models.Model):
    """Modelo para armazenar comentários anônimos sobre os professores."""
    TIPO_CHOICES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='comentarios')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return f"Comentário ({self.tipo}) sobre {self.professor.nome}"
