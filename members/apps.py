from django.apps import AppConfig


def _setup_default_role_groups(sender, **kwargs):
    # Executa quando o app books_tech termina de migrar.
    # Conectamos pelo app members para garantir que o auth já conectou
    # o handler que cria permissões padrão (create_permissions).
    if getattr(sender, 'name', None) != 'books_tech':
        return

    from books_tech.signals import ensure_default_role_groups

    ensure_default_role_groups()


class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members'

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(
            _setup_default_role_groups,
            dispatch_uid='members.setup_default_role_groups',
        )
