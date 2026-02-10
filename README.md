# Blogpost (Django)

Este repositório contém um projeto Django minimalista para um blog pessoal (app principal `books_tech`).
O objetivo é uma base limpa com uma página `home.html` e instruções para você recriar funcionalidades (Post, Usuário customizado, uploads, admin, etc.).
# blogpost

 é um projeto para criar, editar e publicar posts de blog de forma simples e organizada. Este README fornece visão geral, instruções de instalação, uso, desenvolvimento e contribuição para que você e outras pessoas possam trabalhar no repositório com facilidade.

## Descrição
Uma aplicação para gerenciar conteúdo de blog (criação, edição, exclusão, listagem e publicação de posts). Pode ser um site estático, SPA ou uma aplicação full‑stack dependendo da implementação. Este README serve como base e pode ser adaptado ao seu stack (por exemplo: Node.js + Express, Next.js, Gatsby, Hugo, Jekyll, etc).
# Blogpost (Django)

Este repositório contém um projeto Django minimalista para um blog pessoal (app principal `books_tech`).
O objetivo é uma base limpa com uma página `home.html` e instruções para você recriar funcionalidades (Post, Usuário customizado, uploads, admin, etc.).

**Resumo**
 - Projeto Django mínimo para um blog pessoal.
 - App principal: `books_tech` (versão reduzida; arquivos antigos em `books_tech/backup/`).
 - Objetivo atual: manter apenas a homepage funcionando e permitir que você releia ou restaure recursos a partir do backup.

---

Visão geral
 - Propósito: servir como base didática para aprender Django construindo um blog.
 - Estado atual: projeto simplificado; backup completo em `books_tech/backup/` e branch `cleanup-home-only`.

---

**Contents**
 - `devblog/` — projeto Django (settings, urls, wsgi)
 - `books_tech/` — app principal (atualmente reduzido)
 - `books_tech/backup/` — cópia completa dos arquivos removidos
# Blogpost (Django)

Breve
- Projeto Django mínimo para um blog pessoal; atualmente reduzido para servir apenas a homepage.
- Arquivos antigos e versões anteriores estão preservados em `books_tech/backup/` e na branch `cleanup-home-only`.

Estrutura
- `devblog/` — arquivo de configuração do projeto
- `books_tech/` — app principal (reduzido)
- `books_tech/backup/` — arquivos removidos preservados
- `virt/` — virtualenv (opcional)

Uso (resumo)
- Ative seu ambiente virtual e instale dependências, se houver.
- Execute migrações e rode o servidor de desenvolvimento para ver a homepage localmente.

Observações importantes
- Defina `AUTH_USER_MODEL` antes de executar migrações que criem referências ao usuário. Alterações posteriores podem exigir reset do banco e das migrações.
- Se usar um user model customizado, garanta `related_name` exclusivos para campos ManyToMany ligados a `Group` e `Permission` para evitar colisões.

Backups e branches
- Branch de segurança: `cleanup-home-only`.
- Restaure arquivos individuais copiando do diretório `books_tech/backup/` quando necessário.

Próximos passos sugeridos
- Restaurar ou criar o modelo `Post` e aplicar migrações.
- Registrar `Post` no admin e criar um superuser.
- Adicionar suporte a uploads apenas se necessário.

Contribuição e licença
- Use branches por feature e commits pequenos.
- Adicione um arquivo `LICENSE` (ex.: MIT) se pretende compartilhar o projeto.

Se quiser, eu gero um checklist conciso para o próximo passo que escolher (restaurar do backup ou criar apps novos).
