from django.contrib.auth.models import Permission, User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.text import slugify

from .models import Categoria, Comentario, Post


class EditarUsuarioTests(TestCase):
	def setUp(self):
		self.staff = User.objects.create_superuser(
			username='admin_staff',
			email='admin@example.com',
			password='senha_admin_123',
		)
		self.usuario = User.objects.create_user(
			username='usuario_teste',
			password='senha_antiga_123',
			email='antigo@example.com',
		)

	def test_salva_alteracoes_sem_trocar_senha(self):
		self.client.force_login(self.staff)
		senha_hash_antiga = self.usuario.password

		url = reverse('books_tech:editar_usuario', args=[self.usuario.id])
		response = self.client.post(
			url,
			{
				'username': 'usuario_teste',
				'first_name': 'Micael',
				'last_name': 'Silva',
				'email': 'novo@example.com',
				'password': '',
				'confirm_password': '',
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.usuario.refresh_from_db()
		self.assertEqual(self.usuario.first_name, 'Micael')
		self.assertEqual(self.usuario.last_name, 'Silva')
		self.assertEqual(self.usuario.email, 'novo@example.com')
		self.assertEqual(self.usuario.password, senha_hash_antiga)
		self.assertTrue(self.usuario.check_password('senha_antiga_123'))

	def test_troca_senha_quando_informada_e_confirmada(self):
		self.client.force_login(self.staff)
		url = reverse('books_tech:editar_usuario', args=[self.usuario.id])
		response = self.client.post(
			url,
			{
				'username': 'usuario_teste',
				'first_name': '',
				'last_name': '',
				'email': 'antigo@example.com',
				'password': 'senha_nova_456',
				'confirm_password': 'senha_nova_456',
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.usuario.refresh_from_db()
		self.assertTrue(self.usuario.check_password('senha_nova_456'))

	def test_nao_salva_quando_falta_confirmacao(self):
		self.client.force_login(self.staff)
		senha_hash_antiga = self.usuario.password

		url = reverse('books_tech:editar_usuario', args=[self.usuario.id])
		response = self.client.post(
			url,
			{
				'username': 'usuario_teste',
				'first_name': 'NaoDeveSalvar',
				'last_name': '',
				'email': 'antigo@example.com',
				'password': 'senha_nova_999',
				'confirm_password': '',
			},
		)

		self.assertEqual(response.status_code, 200)
		self.usuario.refresh_from_db()
		self.assertEqual(self.usuario.password, senha_hash_antiga)
		self.assertNotEqual(self.usuario.first_name, 'NaoDeveSalvar')

	def test_nao_salva_quando_confirmacao_nao_bate(self):
		self.client.force_login(self.staff)
		senha_hash_antiga = self.usuario.password

		url = reverse('books_tech:editar_usuario', args=[self.usuario.id])
		response = self.client.post(
			url,
			{
				'username': 'usuario_teste',
				'first_name': 'NomeQueNaoDeveSalvar',
				'last_name': '',
				'email': 'antigo@example.com',
				'password': 'abc123',
				'confirm_password': 'xyz999',
			},
		)

		self.assertEqual(response.status_code, 200)
		self.usuario.refresh_from_db()
		self.assertEqual(self.usuario.password, senha_hash_antiga)
		self.assertNotEqual(self.usuario.first_name, 'NomeQueNaoDeveSalvar')

	def test_apenas_staff_pode_acessar_edicao(self):
		url = reverse('books_tech:editar_usuario', args=[self.usuario.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)  # redirect para login

		self.client.force_login(self.usuario)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)
		self.assertIn('notice=', response.url)

	def test_staff_pode_atribuir_permissoes(self):
		self.client.force_login(self.staff)
		perm = Permission.objects.get(content_type__app_label='auth', codename='change_user')

		url = reverse('books_tech:editar_usuario', args=[self.usuario.id])
		response = self.client.post(
			url,
			{
				'username': 'usuario_teste',
				'first_name': '',
				'last_name': '',
				'email': 'antigo@example.com',
				'password': '',
				'confirm_password': '',
				'permissions': [str(perm.id)],
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.usuario.refresh_from_db()
		self.assertTrue(self.usuario.has_perm('auth.change_user'))


class DelUserTests(TestCase):
	def setUp(self):
		self.staff = User.objects.create_superuser(
			username='admin_staff',
			email='admin@example.com',
			password='senha_admin_123',
		)
		self.usuario = User.objects.create_user(
			username='usuario_teste',
			password='senha_usuario_123',
			email='usuario@example.com',
		)

	def test_staff_pode_desativar_usuario(self):
		self.client.force_login(self.staff)
		url = reverse('books_tech:deluser', args=[self.usuario.id])
		response = self.client.post(url, follow=True)

		self.assertEqual(response.status_code, 200)
		self.usuario.refresh_from_db()
		self.assertFalse(self.usuario.is_active)

	def test_nao_staff_nao_pode_desativar_usuario(self):
		self.client.force_login(self.usuario)
		url = reverse('books_tech:deluser', args=[self.staff.id])
		response = self.client.post(url)

		self.assertEqual(response.status_code, 302)
		self.assertIn('notice=', response.url)

	def test_staff_nao_pode_desativar_o_proprio_usuario(self):
		self.client.force_login(self.staff)
		url = reverse('books_tech:deluser', args=[self.staff.id])
		response = self.client.post(url, follow=True)

		self.assertEqual(response.status_code, 200)
		self.staff.refresh_from_db()
		self.assertTrue(self.staff.is_active)

	def test_staff_pode_ativar_usuario_inativo(self):
		self.usuario.is_active = False
		self.usuario.save(update_fields=['is_active'])

		self.client.force_login(self.staff)
		url = reverse('books_tech:activateuser', args=[self.usuario.id])
		response = self.client.post(url, follow=True)

		self.assertEqual(response.status_code, 200)
		self.usuario.refresh_from_db()
		self.assertTrue(self.usuario.is_active)

	def test_nao_staff_nao_pode_ativar_usuario(self):
		self.staff.is_active = False
		self.staff.save(update_fields=['is_active'])

		self.client.force_login(self.usuario)
		url = reverse('books_tech:activateuser', args=[self.staff.id])
		response = self.client.post(url)

		self.assertEqual(response.status_code, 302)
		self.assertIn('notice=', response.url)


class VisitanteLeituraTests(TestCase):
	def setUp(self):
		self.autor = User.objects.create_user(
			username='autor',
			password='senha_autor_123',
			email='autor@example.com',
		)
		self.categoria = Categoria.objects.create(nome='Python e Django')
		self.post = Post.objects.create(
			titulo='Post público',
			autor=self.autor,
			categoria=self.categoria,
			conteudo='Conteúdo do post',
		)

	def test_visitante_pode_ver_home(self):
		url = reverse('books_tech:home_view')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_visitante_pode_ver_detalhe_post(self):
		url = reverse('books_tech:post_detail', args=[self.post.id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_visitante_pode_ver_posts_por_categoria(self):
		url = reverse('books_tech:categoria_posts', args=[slugify(self.categoria.nome)])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_visitante_nao_pode_comentar_quando_desativado(self):
		url = reverse('books_tech:add_comentario', args=[self.post.id])
		response = self.client.post(url, {'texto': 'Comentário visitante'})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(response.url.startswith('/login/'))
		self.assertEqual(Comentario.objects.count(), 0)

	def test_leitor_logado_pode_comentar(self):
		leitor = User.objects.create_user(
			username='leitor',
			password='senha_leitor_123',
			email='leitor@example.com',
		)
		self.client.force_login(leitor)
		url = reverse('books_tech:add_comentario', args=[self.post.id])
		response = self.client.post(url, {'texto': 'Comentário de leitor logado'}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Comentario.objects.count(), 1)
		comentario = Comentario.objects.get()
		self.assertEqual(comentario.post, self.post)
		self.assertEqual(comentario.autor, leitor)

	@override_settings(ALLOW_ANONYMOUS_COMMENTS=True)
	def test_visitante_pode_comentar_quando_ativado(self):
		url = reverse('books_tech:add_comentario', args=[self.post.id])
		response = self.client.post(url, {'texto': 'Comentário visitante'}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Comentario.objects.count(), 1)
		comentario = Comentario.objects.get()
		self.assertEqual(comentario.post, self.post)
		self.assertIsNone(comentario.autor)
