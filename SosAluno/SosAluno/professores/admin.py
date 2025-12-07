from django.contrib import admin
from .models import Professor, Comentario, Instituicao, ComentarioInstituicao, Curso, ComentarioCurso


class ComentarioInline(admin.TabularInline):
    """Inline para editar comentários dentro da página do professor."""
    model = Comentario
    extra = 1
    fields = ('tipo', 'texto', 'criado_em')
    readonly_fields = ('criado_em',)


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    """Admin para o modelo Professor."""
    list_display = ('nome', 'materia', 'instituicao', 'avaliacao_geral', 'total_avaliacoes', 'criado_em')
    list_filter = ('instituicao', 'materia', 'avaliacao_geral', 'criado_em')
    search_fields = ('nome', 'materia', 'instituicao', 'id_slug')
    prepopulated_fields = {'id_slug': ('nome',)}
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = [ComentarioInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id_slug', 'nome', 'foto')
        }),
        ('Detalhes Profissionais', {
            'fields': ('materia', 'instituicao')
        }),
        ('Avaliações', {
            'fields': ('avaliacao_geral', 'total_avaliacoes')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    """Admin para o modelo Comentario."""
    list_display = ('professor', 'tipo', 'criado_em', 'texto_preview')
    list_filter = ('tipo', 'professor', 'criado_em')
    search_fields = ('professor__nome', 'texto')
    readonly_fields = ('criado_em',)
    fieldsets = (
        ('Informações do Comentário', {
            'fields': ('professor', 'tipo', 'texto')
        }),
        ('Datas', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )

    def texto_preview(self, obj):
        """Mostra uma prévia do texto do comentário."""
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_preview.short_description = 'Texto'



# --- Administração de Instituições ---

class ComentarioInstituicaoInline(admin.TabularInline):
    """Inline para editar comentários dentro da página da instituição."""
    model = ComentarioInstituicao
    extra = 1
    fields = ('tipo', 'texto', 'criado_em')
    readonly_fields = ('criado_em',)


class CursoInline(admin.TabularInline):
    """Inline para editar cursos dentro da página da instituição."""
    model = Curso
    extra = 0
    fields = ('id_slug', 'nome', 'area', 'duracao', 'avaliacao_geral')
    readonly_fields = ()


@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    """Admin para o modelo Instituicao."""
    list_display = ('nome', 'localizacao', 'avaliacao_geral', 'total_avaliacoes', 'criado_em')
    list_filter = ('localizacao', 'avaliacao_geral', 'criado_em')
    search_fields = ('nome', 'localizacao', 'id_slug')
    prepopulated_fields = {'id_slug': ('nome',)}
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = [CursoInline, ComentarioInstituicaoInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id_slug', 'nome', 'logo', 'descricao')
        }),
        ('Localização e Contato', {
            'fields': ('localizacao', 'website')
        }),
        ('Avaliações', {
            'fields': ('avaliacao_geral', 'total_avaliacoes')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComentarioInstituicao)
class ComentarioInstituicaoAdmin(admin.ModelAdmin):
    """Admin para o modelo ComentarioInstituicao."""
    list_display = ('instituicao', 'tipo', 'criado_em', 'texto_preview')
    list_filter = ('tipo', 'instituicao', 'criado_em')
    search_fields = ('instituicao__nome', 'texto')
    readonly_fields = ('criado_em',)
    fieldsets = (
        ('Informações do Comentário', {
            'fields': ('instituicao', 'tipo', 'texto')
        }),
        ('Datas', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )

    def texto_preview(self, obj):
        """Mostra uma prévia do texto do comentário."""
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_preview.short_description = 'Texto'


# --- Administração de Cursos ---

class ComentarioCursoInline(admin.TabularInline):
    """Inline para editar comentários dentro da página do curso."""
    model = ComentarioCurso
    extra = 1
    fields = ('tipo', 'texto', 'criado_em')
    readonly_fields = ('criado_em',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    """Admin para o modelo Curso."""
    list_display = ('nome', 'instituicao', 'area', 'duracao', 'avaliacao_geral', 'total_avaliacoes', 'criado_em')
    list_filter = ('instituicao', 'area', 'avaliacao_geral', 'criado_em')
    search_fields = ('nome', 'area', 'id_slug', 'instituicao__nome')
    prepopulated_fields = {'id_slug': ('nome',)}
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = [ComentarioCursoInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id_slug', 'nome', 'descricao')
        }),
        ('Detalhes do Curso', {
            'fields': ('instituicao', 'area', 'duracao')
        }),
        ('Avaliações', {
            'fields': ('avaliacao_geral', 'total_avaliacoes')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComentarioCurso)
class ComentarioCursoAdmin(admin.ModelAdmin):
    """Admin para o modelo ComentarioCurso."""
    list_display = ('curso', 'tipo', 'criado_em', 'texto_preview')
    list_filter = ('tipo', 'curso', 'criado_em')
    search_fields = ('curso__nome', 'texto')
    readonly_fields = ('criado_em',)
    fieldsets = (
        ('Informações do Comentário', {
            'fields': ('curso', 'tipo', 'texto')
        }),
        ('Datas', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )

    def texto_preview(self, obj):
        """Mostra uma prévia do texto do comentário."""
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_preview.short_description = 'Texto'
