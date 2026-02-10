# 📚 Blogpost

Um blog moderno e funcional construído com Django. Publique posts, organize por categorias, interaja com comentários e gerencie seu perfil de autor.

## ⚡ Quick Start

```bash
# Ativar ambiente virtual
source virt/Scripts/activate  # Windows
# ou
source virt/bin/activate      # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

Acesse http://localhost:8000

## 🎯 Funcionalidades

- ✅ **Autenticação**: Login e cadastro de usuários
- ✅ **Posts**: Criar, editar, deletar e publicar posts
- ✅ **Categorias**: Organizador posts por tópicos
- ✅ **Comentários**: Interagir nos posts com comentários
- ✅ **Perfil de Autor**: Página de perfil com foto e bio
- ✅ **Imagens**: Upload de imagens para posts e perfil
- ✅ **Admin**: Painel de admin para gerenciar conteúdo
- ✅ **Timezone**: Horários exibidos em São Paulo (America/Sao_Paulo)
- ✅ **Idioma**: Interface em português

## 📂 Estrutura

```
blogpost/
├── devblog/           # Configuração do projeto
├── books_tech/        # App principal (blog)
├── members/           # App de autenticação
├── static/            # CSS, JS, imagens
├── media/             # Uploads de usuários
├── templates/         # Templates HTML
├── db.sqlite3         # Banco de dados
└── manage.py          # CLI do Django
```

## 🔧 Tecnologias

- **Django 5.1.3** - Framework web
- **Python 3.13** - Linguagem
- **Bootstrap 5.3.8** - CSS framework
- **SQLite** - Banco de dados (dev)

## 👨‍💻 Desenvolvedor

Para adicionar novas features:

1. Crie uma branch: `git checkout -b feature/minha-feature`
2. Faça suas mudanças
3. Teste localmente
4. Envie um pull request

## 📝 Variáveis de Ambiente

Configure em `devblog/settings.py`:

- `DEBUG` - Modo debug (True para desenvolvimento)
- `SECRET_KEY` - Chave secreta do Django
- `TIME_ZONE` - Fuso horário (padrão: America/Sao_Paulo)
- `LANGUAGE_CODE` - Idioma (padrão: pt-br)

## 🚀 Deploy

Para produção, consulte a documentação do Django sobre:
- Configurar `DEBUG = False`
- Usar MySQL em vez de SQLite
- Configurar variáveis de ambiente
- Setup de servidor (Gunicorn, Nginx, etc)
