---
name: criacao-bot-telegram
description: Metodologia para criar e iniciar um novo projeto de bot no Telegram do zero — objetivo, requisitos e decisões, estrutura de pastas, AGENTS.md, CHANGELOG.md, .gitignore, esqueleto de código (bot/), testes e deploy via systemd. Use esta skill sempre que o usuário mencionar criar, começar ou iniciar um bot no Telegram, "novo bot", "bootstrap de bot", "estrutura inicial de bot", "montar o kickoff de um bot" ou preparar os arquivos iniciais (AGENTS.md, CHANGELOG.md) de um projeto de bot, mesmo que não use as palavras "metodologia" ou "skill". Também vale para retomar um bot Telegram recém-criado que ainda não tem estrutura, testes ou documentação.
---

# Criação de Bot Telegram

Metodologia para tirar um bot Telegram do zero e chegar a um projeto estruturado, documentado e
testável. A ideia central: **fechar as decisões estruturais antes de escrever código** e **gerar de
uma vez os artefatos de projeto** (`AGENTS.md`, `CHANGELOG.md`, `.gitignore`, estrutura de pastas),
porque refazer isso depois custa caro.

O resultado esperado ao final do *kickoff* é um repositório que já nasce com:
- objetivo e requisitos registrados (`docs/prompt-inicial.md`, `docs/requisitos.md`);
- contrato de trabalho para agentes (`AGENTS.md`);
- versionamento (`CHANGELOG.md` + política de tags);
- estrutura de código (`bot/`) e ambiente de testes (`pytest`);
- política de backup, de segredos e de publicação controlada.

---

## Quando usar

- O usuário quer **criar/começar um novo bot no Telegram** (com ou sem framework decidido).
- O usuário quer **apenas os arquivos iniciais** (`AGENTS.md`, `CHANGELOG.md`, `.gitignore`, pastas).
- O usuário tem um bot Telegram **recém-criado e sem estrutura/testes/documentação** e quer padronizar.

## Quando NÃO usar

- Alterações pontuais em um bot já estruturado (use o `AGENTS.md` daquele projeto).
- Criar uma skill, agente ou plugin de OpenCode (use `customize-opencode`/`skill-creator`).
- Convenção de `CHANGELOG.md` isolada (carregue `changelog-convention` diretamente).

---

## Princípios (o porquê)

1. **Decisões antes de código.** A maior fonte de retrabalho é o modelo de dados e o alvo das
   alterações do bot. Fechar isso na Fase 1 evita refazer serviços e handlers.
2. **Uma fonte de verdade por assunto.** Escopo em `docs/requisitos.md`; arquitetura no código;
   histórico no `CHANGELOG.md`; convenção de changelog na skill `changelog-convention`.
3. **Backup e aprovação são pré-condição de escrita.** Qualquer bot que altere arquivos/estado deve
   fazer backup antes e pedir confirmação explícita antes de gravar/publicar.
4. **Testes herméticos.** Sem `.env` real, sem rede, sem escrever em arquivos de produção — isolar
   com `tmp_path`/`monkeypatch` e mockar serviços externos.
5. **Reaproveitar arquitetura, não copiar domínio.** O projeto de referência
   `/home/roberto/projetos/agendatipara-bot` serve como **fonte de arquitetura** (somente leitura);
   as regras de negócio mudam a cada bot.

---

## Fluxo (fases 0–7)

Trabalhe as fases em ordem. Os detalhes operacionais de cada tema estão em `references/`.

### Fase 0 — Capturar o objetivo
Produza `docs/prompt-inicial.md` a partir do template `assets/templates/prompt-inicial.template.md`.
Colete: objetivo em uma frase, funcionalidades, menu principal, campos de cada fluxo, integrações,
requisitos de segurança e entregáveis. Se o usuário não souber detalhar, faça perguntas curtas.

### Fase 1 — Consolidar requisitos e decisões
Transforme o prompt em `docs/requisitos.md` (`assets/templates/requisitos.template.md`).
**Não** avance enquanto o modelo de dados, a origem/destino dos dados e as regras de formatação não
estiverem fechados. Ver `references/fase-requisitos.md`.
Marque explicitamente as pendências; toda pergunta de escopo respondida vira uma decisão numerada.

### Fase 2 — Estrutura de pastas + repositório
Crie a árvore base, o `.gitignore` e inicialize o git. O caminho recomendado é rodar
`scripts/bootstrap.py` (ver abaixo); ele monta pastas, `.gitkeep`, `.gitignore`, `pytest.ini`,
`requirements.txt`, `.env.example` e copia os templates.
```bash
python3 scripts/bootstrap.py --project-dir <destino> --name <nome-projeto> \
    --data-dir <pasta-de-dados> --remote <url-do-repo> --date DD/MM/AAAA
```
Use `--dry-run` primeiro para revisar o que será criado.

### Fase 3 — `AGENTS.md`
Gere a partir de `assets/templates/AGENTS.template.md` e **adapte** as seções específicas:
regras de negócio, regiões protegidas, integrações e variáveis de ambiente. Ver
`references/politicas.md` para as políticas (backup, testes, git, risco).

### Fase 4 — `CHANGELOG.md`
Copie `assets/templates/CHANGELOG.template.md` e siga a skill **`changelog-convention`** (não
duplique a convenção aqui). Versão inicial: `v0.1.0`. Tags anotadas: `vX.Y[.Z]` com mensagem
`deploy validado: <resumo>`.

### Fase 5 — Esqueleto de código
Crie `bot/` na ordem: `config.py` + `.env.example` → serviços de dados (com testes) → serviço de
backup → histórico → `models`/`schemas` → `state_manager` → `handlers` → serviço de publicação.
Ver `references/arquitetura-bot.md`.

### Fase 6 — Testes
Cada serviço crítico nasce com teste hermético. Detalhes e regras obrigatórias de isolamento em
`references/politicas.md`. Valide com `pytest bot/tests/ -v`.

### Fase 7 — Documentação e deploy
`README.md` (objetivo, instalação, `.env`, comandos, fluxo, backup, deploy, rollback) e deploy via
systemd. Ver `references/deploy-systemd.md`.

---

## Checklist de kickoff

```
[ ] 1. docs/prompt-inicial.md (objetivo + requisitos)
[ ] 2. docs/requisitos.md + decisões estruturais fechadas
[ ] 3. Estrutura de pastas + .gitignore + .gitkeep
[ ] 4. git init -b main + remote origin
[ ] 5. AGENTS.md adaptado ao domínio
[ ] 6. CHANGELOG.md (v0.1.0) conforme changelog-convention
[ ] 7. bot/config.py + bot/.env.example + requirements.txt + pytest.ini
[ ] 8. Primeiro commit (sob autorização) + tag v0.1.0
```

---

## Erros comuns (anti-padrões)

- **Codar antes de fechar o modelo de dados** → retrabalho em serviços e handlers.
- **Misturar escopo em vários documentos** → escolha `docs/requisitos.md` como fonte canônica.
- **Registrar segredos no git** → `.env` sempre no `.gitignore`; `.env.example` sem valores reais.
- **Testar escrevendo em arquivos de produção** → sempre `tmp_path` + `monkeypatch`.
- **Travar o `ConversationHandler` com `CallbackQueryHandler` global** → ver `references/politicas.md`.
- **Reimplementar a convenção de changelog** → referencie a skill `changelog-convention`.

---

## Recursos da skill

- `references/fase-requisitos.md` — como conduzir requisitos, decisões e pendências.
- `references/arquitetura-bot.md` — estrutura `bot/` e padrões de código.
- `references/politicas.md` — backup, testes herméticos, git, `ConversationHandler`, risco.
- `references/deploy-systemd.md` — unit, venv, restart, instância única, rollback.
- `assets/templates/` — modelos prontos para copiar (ver `assets/templates/README.md`).
- `scripts/bootstrap.py` — scaffold idempotente (pastas + templates), com `--dry-run`.
- `evals/evals.json` — casos de teste da própria skill.

## Referências externas

- Arquitetura/padrões: `/home/roberto/projetos/agendatipara-bot` (**somente leitura**).
- Convenção de changelog: skill `changelog-convention`.
- Criação de skills: skill `skill-creator`.
