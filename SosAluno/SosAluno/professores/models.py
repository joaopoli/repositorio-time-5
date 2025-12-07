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


class Instituicao(models.Model):
    """Modelo para armazenar informações das instituições."""
    id_slug = models.SlugField(unique=True, max_length=100, help_text="ID único da instituição (ex: puc-rio)")
    nome = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='instituicoes/', null=True, blank=True)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=300)
    website = models.URLField(max_length=300, blank=True)
    avaliacao_geral = models.FloatField(default=0.0, help_text="Avaliação de 0 a 5")
    total_avaliacoes = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-avaliacao_geral']
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.nome


class ComentarioInstituicao(models.Model):
    """Modelo para armazenar comentários anônimos sobre as instituições."""
    TIPO_CHOICES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]

    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name='comentarios')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = "Comentário de Instituição"
        verbose_name_plural = "Comentários de Instituições"

    def __str__(self):
        return f"Comentário ({self.tipo}) sobre {self.instituicao.nome}"


class Curso(models.Model):
    """Modelo para armazenar informações dos cursos."""
    id_slug = models.SlugField(unique=True, max_length=100, help_text="ID único do curso (ex: engenharia-software)")
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    duracao = models.CharField(max_length=100, help_text="Ex: 4 anos, 6 semestres")
    area = models.CharField(max_length=200, help_text="Ex: Engenharia, Ciências Humanas")
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name='cursos')
    avaliacao_geral = models.FloatField(default=0.0, help_text="Avaliação de 0 a 5")
    total_avaliacoes = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-avaliacao_geral']
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return f"{self.nome} - {self.instituicao.nome}"


class ComentarioCurso(models.Model):
    """Modelo para armazenar comentários anônimos sobre os cursos."""
    TIPO_CHOICES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='comentarios')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = "Comentário de Curso"
        verbose_name_plural = "Comentários de Cursos"

    def __str__(self):
        return f"Comentário ({self.tipo}) sobre {self.curso.nome}"
