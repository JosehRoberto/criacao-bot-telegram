# Prompt inicial — <NOME_PROJETO>

> Cole este conteúdo como ponto de partida do projeto. Preencha os `<...>`.

Crie um novo bot Telegram reutilizando a arquitetura, padrões de código, fluxo conversacional,
validação, preview, aprovação e organização de handlers do projeto
`/home/roberto/projetos/agendatipara-bot`.

## Objetivo do novo bot

<DESCREVA_EM_UMA_FRASE_O_QUE_O_BOT_RESOLVE>

O bot deve permitir: <FUNCIONALIDADES>.

## Requisitos obrigatórios

1. Operar sobre <FONTE_DE_DADOS> (clone/arquivo local).
2. Antes de qualquer modificação, criar backup em `backup/` no padrão
   `backup/<nome>_YYYYMMDD_HHMMSS.bak`.
3. Ler e interpretar o alvo preservando integralmente estrutura, títulos, seções, ordem e formatação.
4. Menu principal no Telegram com: <OPÇÕES>.
5. Fluxo de cadastro com os campos: <CAMPOS>.
6. Validar: campos obrigatórios, formatos, duplicidade e consistência do resultado.
7. Enviar **preview** e permitir: ✅ Aprovar · ✏️ Editar · 🔀 Trocar seção · ❌ Cancelar.
8. Somente após aprovação explícita: criar backup, aplicar a alteração e registrar no histórico.
9. Alteração **cirúrgica** — sem reformatar outras partes.
10. Publicação (`/publicar`) como etapa separada: commit local, branch+commit, push, Merge Request —
    sempre com confirmação explícita.
11. Restringir a usuários autorizados por `TELEGRAM_ALLOWED_USER_IDS`.
12. Segredos apenas em `.env`, com `.env.example` documentado.
13. Testes automatizados (pytest, herméticos) para os serviços críticos.
14. Documentar em `README.md`: objetivo, instalação, `.env`, comandos, fluxo, estrutura, backup,
    deploy systemd e rollback.

## Entregáveis esperados

- Estrutura completa do projeto · código-fonte funcional · parser/editor seguro · handlers ·
  modelo de dados · serviços de backup, histórico e publicação · testes · `.env.example` ·
  `README.md` · `CHANGELOG.md` inicial.
