from __future__ import annotations

from django.contrib.auth.models import Group, Permission


ROLE_GROUPS: dict[str, list[str]] = {
    # Leitor logado: pode comentar.
    'Leitor': [
        'add_comentario',
    ],
    # Autor: pode publicar e gerenciar os próprios posts + editar o perfil de autor.
    'Autor': [
        'add_comentario',
        'add_post',
        'change_post',
        'delete_post',
        'add_perfilautor',
        'change_perfilautor',
    ],
}


def ensure_default_role_groups() -> None:
    """Garante que os grupos de papel existam e tenham permissões padrão.

    Executa de forma idempotente.
    """

    for group_name, codenames in ROLE_GROUPS.items():
        group, _ = Group.objects.get_or_create(name=group_name)

        perms = Permission.objects.filter(
            content_type__app_label='books_tech',
            codename__in=codenames,
        )

        # Mantém o grupo coerente com a definição do papel.
        group.permissions.set(perms)
