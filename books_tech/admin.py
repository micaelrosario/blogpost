from django.contrib import admin
from django.utils.html import format_html
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'autor', 'criado_em', 'thumbnail')
	ordering = ('-criado_em',)
	readonly_fields = ('thumbnail',)

	def thumbnail(self, obj):
		if obj.imagem:
			return format_html('<img src="{}" style="width: 100px; height: auto;"/>', obj.imagem.url)
		return '(sem imagem)'

	thumbnail.short_description = 'Imagem'
