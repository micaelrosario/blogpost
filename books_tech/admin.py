from django.contrib import admin
from .models import Post, Categoria, Comentario, PerfilAutor

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'criado_em', 'autor')
	search_fields = ('titulo', 'conteudo')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
	list_display = ('post', 'autor', 'criado_em')
	search_fields = ('texto',)

@admin.register(PerfilAutor)
class PerfilAutorAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'bio')
	search_fields = ('usuario__username', 'bio')