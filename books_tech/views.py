from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.views import LoginView, redirect_to_login
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import (
    CategoriaForm,
    ComentarioForm,
    EditForm,
    LoginForm,
    PerfilAutorForm,
    PostForm,
    UsuarioForm,
)
from .models import Categoria, Comentario, PerfilAutor, Post


def _redirect_home_with_notice(message: str, level: str = 'danger'):
    params = urlencode({'notice': message, 'level': level})
    return redirect(f"{reverse_lazy('books_tech:home_view')}?{params}")


class FriendlyPermissionRequiredMixin(PermissionRequiredMixin):
    """Evita 403 cru: redireciona com aviso amigável."""

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        return _redirect_home_with_notice('Você não tem permissão para realizar esta ação.', 'danger')


class HomeView(ListView):

    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        # Consome mensagens pendentes para evitar que apareçam na Home.
        from django.contrib.messages import get_messages

        list(get_messages(request))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notice = (self.request.GET.get('notice') or '').strip()
        level = (self.request.GET.get('level') or 'info').strip().lower()

        allowed_levels = {'success', 'danger', 'warning', 'info'}
        if level not in allowed_levels:
            level = 'info'

        context['home_notice'] = notice
        context['home_notice_level'] = level
        return context


def CategoryView(request, category_name):
    from django.utils.text import slugify

    # Busca a categoria comparando os slugs
    all_categories = Categoria.objects.all()
    category = None

    for cat in all_categories:
        if slugify(cat.nome) == category_name:
            category = cat
            break

    if category:
        posts = Post.objects.filter(categoria=category).order_by('-criado_em')
        return render(request, 'categoria_posts.html', {'posts': posts, 'category': category})

    return render(request, '404.html', status=404)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allow_anonymous_comments'] = bool(getattr(settings, 'ALLOW_ANONYMOUS_COMMENTS', False))
        return context

    def get(self, request, *args, **kwargs):
        from django.http import Http404

        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except Http404:
            return render(request, '404.html', status=404)


class PostCreateView(LoginRequiredMixin, FriendlyPermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = '/'
    login_url = '/login/'
    permission_required = 'books_tech.add_post'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, FriendlyPermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = EditForm
    success_url = '/'
    login_url = '/login/'
    permission_required = 'books_tech.change_post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.autor != self.request.user and not self.request.user.is_superuser:
            messages.error(self.request, 'Você não tem permissão para editar este post.')
            return None

        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return _redirect_home_with_notice('Você não tem permissão para editar este post.', 'danger')

        self.object = obj
        return super().dispatch(request, *args, **kwargs)


@login_required
def delete_post_direct(request, pk):
    if not request.user.has_perm('books_tech.delete_post'):
        return _redirect_home_with_notice('Você não tem permissão para apagar posts.', 'danger')

    post = get_object_or_404(Post, pk=pk)
    if post.autor != request.user and not request.user.is_superuser:
        return _redirect_home_with_notice('Você não tem permissão para apagar este post (apenas o autor pode).', 'danger')

    post.delete()
    return _redirect_home_with_notice('Post apagado com sucesso!', 'success')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    # redirect_authenticated_user = True

    def get_success_url(self):
        return '/'


@login_required(login_url='/login/')
def admin_panel(request):
    if not request.user.is_superuser:
        return _redirect_home_with_notice('Você não tem permissão para acessar o painel administrativo.', 'danger')

    users = list(User.objects.all().prefetch_related('groups').order_by('username'))
    for u in users:
        if u.is_superuser:
            u.role_label = 'Administrador'
            continue

        group_names = {g.name for g in u.groups.all()}
        if 'Autor' in group_names:
            u.role_label = 'Autor'
        elif 'Leitor' in group_names:
            u.role_label = 'Leitor'
        else:
            # Papel padrão (fallback seguro para usuários antigos sem grupo).
            u.role_label = 'Leitor'

    role_order = {
        'Administrador': 0,
        'Autor': 1,
        'Leitor': 2,
    }

    def _sort_key(user: User):
        is_current_user = 0 if user.id == request.user.id else 1
        is_admin = 0 if user.is_superuser else 1
        role_rank = role_order.get(getattr(user, 'role_label', ''), 99)
        return (is_current_user, is_admin, role_rank, (user.username or '').lower())

    users.sort(key=_sort_key)

    context = {
        'users': users,
        'current_user_id': request.user.id,
    }
    return render(request, 'painel_admin.html', context)


@login_required(login_url='/login/')
def editarusuario(request, id):
    if not request.user.is_superuser:
        return _redirect_home_with_notice('Você não tem permissão para editar usuários.', 'danger')

    usuario = get_object_or_404(User, id=id)

    # Papéis (grupos)
    leitor_group, _ = Group.objects.get_or_create(name='Leitor')
    autor_group, _ = Group.objects.get_or_create(name='Autor')

    if usuario.groups.filter(id=autor_group.id).exists():
        current_role = 'Autor'
    elif usuario.groups.filter(id=leitor_group.id).exists():
        current_role = 'Leitor'
    else:
        current_role = 'Leitor'

    all_permissions = Permission.objects.select_related('content_type').order_by(
        'content_type__app_label',
        'content_type__model',
        'codename',
    )

    permission_groups = []
    current_key = None
    current_group = None
    for perm in all_permissions:
        ct = perm.content_type
        key = f'{ct.app_label}.{ct.model}'
        if key != current_key:
            current_key = key
            current_group = {
                'key': key,
                'label': f'{ct.app_label} / {ct.model}',
                'perms': [],
            }
            permission_groups.append(current_group)

        current_group['perms'].append(perm)

    assigned_permission_ids = set(usuario.user_permissions.values_list('id', flat=True))

    if request.method == 'POST':
        posted_role = (request.POST.get('role') or '').strip()
        if posted_role in {'Leitor', 'Autor'}:
            current_role = posted_role

        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_atualizado = form.save()

            selected_role = (request.POST.get('role') or '').strip()
            if selected_role == 'Autor':
                usuario_atualizado.groups.add(autor_group)
                usuario_atualizado.groups.remove(leitor_group)
            else:
                usuario_atualizado.groups.add(leitor_group)
                usuario_atualizado.groups.remove(autor_group)

            selected_permission_ids = request.POST.getlist('permissions')
            try:
                selected_permission_ids = [int(pid) for pid in selected_permission_ids]
            except (TypeError, ValueError):
                selected_permission_ids = []

            selected_permissions = Permission.objects.filter(id__in=selected_permission_ids)
            usuario_atualizado.user_permissions.set(selected_permissions)

            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('books_tech:admin_panel')

        messages.error(request, 'Erro ao atualizar usuário. Verifique os dados informados.')
    else:
        form = UsuarioForm(instance=usuario)

    context = {
        'formUsuario': form,
        'id': id,
        'current_role': current_role,
        'permission_groups': permission_groups,
        'assigned_permission_ids': assigned_permission_ids,
        'usuario': usuario,
    }
    return render(request, 'editar_usuario.html', context)


@login_required(login_url='/login/')
def deluser(request, id):
    if not request.user.is_superuser:
        return _redirect_home_with_notice('Você não tem permissão para gerenciar usuários.', 'danger')

    if request.method != 'POST':
        return redirect('books_tech:admin_panel')

    usuario = get_object_or_404(User, id=id)

    if usuario == request.user:
        messages.error(request, 'Você não pode desativar seu próprio usuário.')
        return redirect('books_tech:admin_panel')

    if usuario.is_superuser and User.objects.filter(is_superuser=True, is_active=True).count() <= 1:
        messages.error(request, 'Você não pode desativar o último administrador do sistema.')
        return redirect('books_tech:admin_panel')

    if not usuario.is_active:
        messages.info(request, 'Este usuário já está inativo.')
        return redirect('books_tech:admin_panel')

    usuario.is_active = False
    usuario.save(update_fields=['is_active'])

    messages.success(request, 'Usuário desativado com sucesso!')
    return redirect('books_tech:admin_panel')


@login_required(login_url='/login/')
def activateuser(request, id):
    if not request.user.is_superuser:
        return _redirect_home_with_notice('Você não tem permissão para gerenciar usuários.', 'danger')

    if request.method != 'POST':
        return redirect('books_tech:admin_panel')

    usuario = get_object_or_404(User, id=id)

    if usuario == request.user:
        messages.error(request, 'Você não pode alterar o status do seu próprio usuário.')
        return redirect('books_tech:admin_panel')

    if usuario.is_active:
        messages.info(request, 'Este usuário já está ativo.')
        return redirect('books_tech:admin_panel')

    usuario.is_active = True
    usuario.save(update_fields=['is_active'])

    messages.success(request, 'Usuário ativado com sucesso!')
    return redirect('books_tech:admin_panel')


class CategoriaCreateView(LoginRequiredMixin, FriendlyPermissionRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'add_categoria.html'
    success_url = reverse_lazy('books_tech:add_categoria')
    login_url = '/login/'
    permission_required = 'books_tech.add_categoria'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all().order_by('nome')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Categoria adicionada com sucesso!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível adicionar a categoria. Verifique o nome informado.')
        return super().form_invalid(form)


@login_required(login_url='/login/')
def update_categoria(request, pk):
    if not request.user.has_perm('books_tech.change_categoria'):
        return _redirect_home_with_notice('Você não tem permissão para editar categorias.', 'danger')

    if request.method != 'POST':
        return redirect('books_tech:add_categoria')

    categoria = get_object_or_404(Categoria, pk=pk)
    novo_nome = (request.POST.get('nome') or '').strip()

    if not novo_nome:
        messages.error(request, 'O nome da categoria não pode ficar vazio.')
        return redirect('books_tech:add_categoria')

    categoria.nome = novo_nome
    try:
        categoria.save()
        messages.success(request, 'Categoria atualizada com sucesso!')
    except IntegrityError:
        messages.error(request, 'Já existe uma categoria com esse nome.')

    return redirect('books_tech:add_categoria')


@login_required(login_url='/login/')
def delete_categoria(request, pk):
    if not request.user.has_perm('books_tech.delete_categoria'):
        return _redirect_home_with_notice('Você não tem permissão para excluir categorias.', 'danger')

    if request.method != 'POST':
        return redirect('books_tech:add_categoria')

    categoria = get_object_or_404(Categoria, pk=pk)
    categoria.delete()
    messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('books_tech:add_categoria')


class PerfilAutorCreateView(LoginRequiredMixin, FriendlyPermissionRequiredMixin, CreateView):
    model = PerfilAutor
    form_class = PerfilAutorForm
    template_name = 'perfil_autor_form.html'
    success_url = '/'
    login_url = '/login/'
    permission_required = 'books_tech.add_perfilautor'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class PerfilAutorProfile(LoginRequiredMixin, DetailView):
    model = PerfilAutor
    template_name = 'author_profile.html'
    context_object_name = 'perfil_autor'
    login_url = '/login/'

    def get_object(self, queryset=None):
        """Retorna o perfil do autor do usuário atual."""
        try:
            return PerfilAutor.objects.get(usuario=self.request.user)
        except PerfilAutor.DoesNotExist:
            messages.info(self.request, 'Você ainda não tem um perfil de autor. Complete seu perfil para aparecer aqui.')
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect('edit_profile')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@login_required(login_url='/login/')
def perfil_autor_redirect(request):
    # Mantém compatibilidade com a rota antiga, mas a edição agora é unificada.
    return redirect('edit_profile')


class AddComentarioView(CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'post_detail.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        # Esta view existe apenas para POST do formulário de comentário.
        if request.method != 'POST':
            return redirect('books_tech:post_detail', pk=kwargs.get('post_id'))

        if not request.user.is_authenticated and not bool(
            getattr(settings, 'ALLOW_ANONYMOUS_COMMENTS', False)
        ):
            return redirect_to_login(request.get_full_path(), login_url=self.login_url)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.autor = self.request.user
        else:
            form.instance.autor = None
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível adicionar o comentário. Verifique o texto informado.')
        return redirect('books_tech:post_detail', pk=self.kwargs.get('post_id'))


class ComentarioDeleteView(LoginRequiredMixin, FriendlyPermissionRequiredMixin, DeleteView):
    model = Comentario
    login_url = '/login/'
    permission_required = 'books_tech.delete_comentario'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def get_object(self, queryset=None):
        comentario = super().get_object(queryset)
        if comentario.autor != self.request.user and not self.request.user.is_superuser:
            messages.error(self.request, 'Você não tem permissão para deletar este comentário.')
            return None
        return comentario

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return _redirect_home_with_notice('Você não tem permissão para deletar este comentário.', 'danger')
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Comentário deletado com sucesso!')
        return redirect(success_url)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, 'Você não tem permissão para deletar comentários.')
        try:
            comentario = Comentario.objects.get(pk=self.kwargs.get('pk'))
            return redirect(comentario.post.get_absolute_url())
        except Comentario.DoesNotExist:
            return _redirect_home_with_notice('Você não tem permissão para deletar comentários.', 'danger')


class ComentarioUpdateView(LoginRequiredMixin, FriendlyPermissionRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario_edit.html'
    context_object_name = 'comentario'
    login_url = '/login/'
    permission_required = 'books_tech.change_comentario'

    def get_object(self, queryset=None):
        comentario = super().get_object(queryset)
        if comentario.autor != self.request.user and not self.request.user.is_superuser:
            messages.error(self.request, 'Você não tem permissão para editar este comentário.')
            return None
        return comentario

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            try:
                comentario = Comentario.objects.get(pk=kwargs.get('pk'))
                return redirect(comentario.post.get_absolute_url())
            except Comentario.DoesNotExist:
                return _redirect_home_with_notice('Você não tem permissão para editar este comentário.', 'danger')

        self.object = obj
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Comentário atualizado com sucesso!')
        return self.object.post.get_absolute_url()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, 'Você não tem permissão para editar comentários.')
        try:
            comentario = Comentario.objects.get(pk=self.kwargs.get('pk'))
            return redirect(comentario.post.get_absolute_url())
        except Comentario.DoesNotExist:
            return _redirect_home_with_notice('Você não tem permissão para editar comentários.', 'danger')


def logout_view(request):
    logout(request)
    return redirect('books_tech:login')
