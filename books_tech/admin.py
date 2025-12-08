from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'criado_em', 'autor')
	search_fields = ('titulo', 'conteudo')