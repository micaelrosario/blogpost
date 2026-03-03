from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission


class EditarUsuarioTests(TestCase):
	def setUp(self):
		self.staff = User.objects.create_user(
			username='admin_staff',
			password='senha_admin_123',
			email='admin@example.com',
			is_staff=True,
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
