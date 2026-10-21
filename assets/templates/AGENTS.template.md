# AGENTS.md — Guia de Operação para Agentes de IA

## Projeto: <NOME_PROJETO>

> **Este arquivo deve ser lido antes de qualquer alteração no projeto.**
> Escopo e decisões detalhadas: `docs/requisitos.md` (fonte canônica do escopo).
> Idioma do projeto: **português do Brasil (pt-BR)**.

---

## 0. Contexto e repositórios

- **Repositório do projeto (código do bot e docs):** `<REMOTE_URL>` (`origin`).
- **Fonte de dados / alvo das alterações:** `<DESCREVER_E_CAMINHO_OU_URL>`.
- **Projeto de referência (arquitetura/padrões):**
  `/home/roberto/projetos/agendatipara-bot` — **somente leitura**, nunca editar.
- **Finalidade:** <OBJETIVO_EM_UMA_FRASE>.

---

## 1. Estrutura do projeto

```
<NOME_PROJETO>/
├── AGENTS.md
├── CHANGELOG.md
├── README.md
├── .gitignore
├── bot/                     ← código (handlers/models/schemas/services/tests)
├── backup/                  ← backups de arquivos alterados (não versionar *.bak)
├── docs/                    ← requisitos, prompts, planejamentos
└── <PASTA_DE_DADOS>/        ← fonte de dados do bot (se houver) — ignorada no git
```

---

## 2. Política de backup — OBRIGATÓRIA

**Todo arquivo de produção alterado deve ser copiado para `backup/` antes da alteração.**

- Formato: `backup/<nome>_YYYYMMDD_HHMMSS.bak` (fuso `America/Belem`).
- Vários arquivos da mesma operação usam o **mesmo timestamp**.
- Rollback: `cp backup/<nome>_<TS>.bak <caminho-original>`.
- Manter as últimas 5 sessões; **não** commitar `backup/` nem `*.bak`.

---

## 3. Fonte de dados e regiões protegidas

- `<PASTA_DE_DADOS>/` é a **fonte da verdade**; editar apenas o alvo definido e **preservar** os
  demais arquivos.

### 3.1 Regiões protegidas

| Arquivo / Módulo | Região | Motivo |
|---|---|---|
| `bot/services/` | parser/editor do alvo | preservação de estrutura/formatação |
| `bot/services/` | serviço de backup | pré-condição de toda escrita |
| `bot/services/` | serviço de histórico | rastreabilidade |
| `bot/services/` | serviço de publicação (git/API) | commit/branch/push/MR |
| `bot/handlers/` | `create_application()` | ordem de registro dos handlers |
| `bot/handlers/` | orquestração de aprovação/preview | único ponto pós-confirmação |
| `bot/config.py` | leitura de `.env` | sem valores hardcoded |

**Regra:** ao modificar região protegida, adicionar comentário `# ALTERADO [data]: <motivo>`.

---

## 4. Regras de negócio

- <INVARIANTES_DO_DOMINIO: ordenação, formatação, unicidade, marcadores>.
- Alteração **cirúrgica**: nunca reformatar outras partes do alvo.

---

## 5. Autenticação, segredos e `.env`

| Arquivo | Regra |
|---|---|
| `bot/.env` | **Nunca** exibir, logar ou commitar |
| `bot/.env.example` | Manter atualizado, sem valores reais |
| `bot/config.py` | Lê `.env`; sem valores hardcoded |

- Configurar o logger `httpx`/`httpcore` em `WARNING` para o token do Telegram não vazar em logs.
- Autenticação de serviços externos via variáveis de ambiente — **nunca** embutir token em URL.
- Variáveis: <LISTAR>.

---

## 6. Convenções de código

- Reaproveitar padrões do `agendatipara-bot`: `python-telegram-bot>=20`, `pydantic>=2`,
  `python-dotenv`, `requests`, `pytest`.
- Organização: `bot/handlers`, `bot/models`, `bot/schemas`, `bot/services`, `bot/tests`,
  `bot/config.py`, `bot/main.py`.
- Comentários e documentação em pt-BR; sem comentários supérfluos.

---

## 7. Testes e isolamento (OBRIGATÓRIO)

```bash
pytest bot/tests/ -v
pytest bot/tests/ --cov=bot --cov-report=term-missing
```

- Testes **herméticos**: sem `.env` real, sem rede, sem escrita em produção.
- Isolar caminhos com `tmp_path` + `monkeypatch`; mockar serviços externos (`requests`, `git`,
  Telegram).

---

## 8. Handlers e `ConversationHandler`

- **Nunca** registrar `CallbackQueryHandler` global para callbacks tratados no `ConversationHandler`.
- A ordem dos estados vive no `state_manager`; mudá-la exige atualizar perguntas e preview.
- `post_init` atribuído uma única vez em `create_application()`.

---

## 9. Validação após alterações

```bash
python3 -m py_compile bot/<arquivo>.py
python3 -c "from bot.handlers.commands import create_application; print('OK')"
pytest bot/tests/ -v
git status --short
```

---

## 10. Regras para planejamento estratégico

Todo planejamento deve terminar com `## Arquivos que serão alterados ou consultados` e apresentar,
para aprovação explícita: arquivos criados/modificados, dependências e edge cases.

---

## 11. Checklist de alteração

**Antes:** backups criados · região protegida? · segredos? · `ConversationHandler`? · rollback? ·
testes isolados?
**Depois:** `py_compile` · imports · testes · documentação · mensagem de commit sugerida.

---

## 12. Política de Git

- **Commit só sob solicitação** (`feat`, `fix`, `refactor`, `docs`, `chore`, `test`).
- Um commit por tema. Nunca commitar `.env`, dados clonados, `backup/`, `*.bak`, caches.
- Tags anotadas `vX.Y[.Z]` — mensagem `deploy validado: <resumo>`.
- Rollback: `git revert` (preferencial) ou `git checkout <tag> -- <arquivo>`.
- Operações no recurso de destino (git/API) exigem confirmação explícita no Telegram.

---

## 13. Deploy (systemd)

- Venv dedicada; unit `bot/<nome>-bot.service`; `ExecStart=.venv/bin/python -m bot.main`.
- Aplicar = reiniciar o serviço (commit **não** faz deploy). Instância única (evitar `409`).
- Ver `references/deploy-systemd.md` da skill `criacao-bot-telegram`.

---

## 14. Protocolos por tipo de tarefa

- **Diagnóstico:** explicar atual × esperado × divergência; corrigir só após confirmação.
- **Refatoração:** um critério, comportamento preservado, comentar cada mudança.
- **Risco:** baixo (texto/log) → aplicar; médio (handlers) → validar; alto
  (`ConversationHandler`/parser/modelo) → testar fluxo completo.

---

## 15. CHANGELOG e versionamento

- Seguir a skill `changelog-convention`: `## [Unreleased]` no topo, marcos
  `### vX.Y[.Z] (DD/MM/AAAA) — Título`, `## Legenda` no fim; ordem decrescente; sem duplicatas.
- Versão inicial `v0.1.0`; tags anotadas `vX.Y[.Z]` (`deploy validado: <resumo>`).

---

## 16. Encerramento de sessão

Resumo estruturado (pt-BR): o que foi feito · documentação atualizada · pendências · decisões ·
ponto de entrada da próxima sessão. Sugerir mensagem de commit sem commitar.

---

## 17. Execução segura

Etapas pequenas e verificáveis; nada de código parcial; após truncamento, inspecionar antes de
continuar; validar sintaxe/imports/testes antes de concluir.

---

## 18. O próprio AGENTS.md é versionado

Alterações neste arquivo seguem as mesmas regras do projeto. O histórico fica no `CHANGELOG.md` e no git.
