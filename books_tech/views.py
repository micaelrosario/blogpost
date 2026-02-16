from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import PostForm, EditForm, ClearableFileInput, LoginForm, CategoriaForm, PerfilAutorForm, ComentarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Categoria, PerfilAutor, Comentario
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from urllib.parse import urlencode



class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login/'

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

@login_required(login_url='/login/')
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
    else:
        return render(request, '404.html', status=404)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        from django.http import Http404
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except Http404:
            return render(request, '404.html', status=404)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = '/'  
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = EditForm 
    success_url = '/'  
    login_url = '/login/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.autor != self.request.user:
            messages.error(self.request, 'Você não tem permissão para editar este post.')
            return None

        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj is None:
            return redirect('books_tech:home_view')

        self.object = obj
        return super().dispatch(request, *args, **kwargs)


@login_required
def delete_post_direct(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.autor != request.user:
        params = urlencode({
            'notice': 'Você não tem permissão para apagar este post (apenas o autor pode).',
            'level': 'danger',
        })
        return redirect(f"{reverse_lazy('books_tech:home_view')}?{params}")

    post.delete()
    params = urlencode({'notice': 'Post apagado com sucesso!', 'level': 'success'})
    return redirect(f"{reverse_lazy('books_tech:home_view')}?{params}")



#--------------------------------------------------------------------------

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    #redirect_authenticated_user = True

    def get_success_url(self):
        return '/'
    
#----------------------------------------------------------------------------------

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'add_categoria.html'
    success_url = reverse_lazy('books_tech:add_categoria')
    login_url = '/login/'  

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
    if request.method != 'POST':
        return redirect('books_tech:add_categoria')

    categoria = get_object_or_404(Categoria, pk=pk)
    categoria.delete()
    messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('books_tech:add_categoria')



#----------------------------------------------------------------------------------

class PerfilAutorCreateView(LoginRequiredMixin, CreateView):
    model = PerfilAutor
    form_class = PerfilAutorForm
    template_name = 'perfil_autor_form.html'
    success_url = '/'
    login_url = '/login/'  

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
            # Se não existir perfil, redireciona para criar
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
#----------------------------------------------------------------------------------


class AddComentarioView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'post_detail.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

#----------------------------------------------------------------------------------
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    login_url = '/login/'

    def get_success_url(self):
        # Redireciona de volta ao post após deletar o comentário
        return self.object.post.get_absolute_url()

    def get_object(self, queryset=None):
        comentario = super().get_object(queryset)
        if comentario.autor != self.request.user:
            messages.error(self.request, 'Você não tem permissão para deletar este comentário.')
            return None
        return comentario

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect('books_tech:home_view')
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Comentário deletado com sucesso!')
        return redirect(success_url)


class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario_edit.html'
    context_object_name = 'comentario'
    login_url = '/login/'

    def get_object(self, queryset=None):
        comentario = super().get_object(queryset)
        if comentario.autor != self.request.user:
            messages.error(self.request, 'Você não tem permissão para editar este comentário.')
            return None
        return comentario

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            # Se não tiver permissão (ou não existir), volta ao post quando possível
            try:
                comentario = Comentario.objects.get(pk=kwargs.get('pk'))
                return redirect(comentario.post.get_absolute_url())
            except Exception:
                return redirect('books_tech:home_view')

        self.object = obj
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Comentário atualizado com sucesso!')
        return self.object.post.get_absolute_url()

#----------------------------------------------------------------------------------

def logout_view(request):
    logout(request)
    return redirect('books_tech:login')