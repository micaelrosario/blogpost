from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistroDefaultPermissoesTests(TestCase):
	def test_usuario_registrado_recebe_permissao_de_comentar(self):
		url = reverse('register')
		response = self.client.post(
			url,
			{
				'username': 'leitor_novo',
				'password1': 'SenhaForte_12345',
				'password2': 'SenhaForte_12345',
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		user = User.objects.get(username='leitor_novo')
		self.assertTrue(user.groups.filter(name='Leitor').exists())
		self.assertTrue(user.has_perm('books_tech.add_comentario'))
