from django.contrib import admin
from .models import Professor, Comentario


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
