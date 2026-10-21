# Requisitos — <NOME_PROJETO>

Documento de requisitos e decisões do projeto. Consolida o `docs/prompt-inicial.md` e as respostas
de definição de escopo. É a **fonte canônica do escopo**.

- Repositório do projeto: `<REMOTE_URL>`
- Fonte de dados / alvo: `<DESCREVER_CAMINHO_OU_URL>`
- Projeto de referência (arquitetura): `/home/roberto/projetos/agendatipara-bot`

---

## 1. Visão geral

<OBJETIVO_EM_UM_PARAGRAFO>

---

## 2. Decisões confirmadas

### 2.1 Escopo dos dados
- <CAMPO_1>: <decisão>
- <CAMPO_2>: <decisão>

### 2.2 Repositórios e pastas
- Projeto: `<REMOTE_URL>` (`origin`).
- Fonte de dados: `<PASTA_DE_DADOS>/` (clone/estado) — fonte da verdade.
- `backup/`: backups (`<nome>_YYYYMMDD_HHMMSS.bak`).

### 2.3 Localização do código
- Código em `bot/` (handlers/models/schemas/services/tests).

### 2.4 Formato/regras de negócio
- <ORDENAÇÃO>, <FORMATAÇÃO>, <UNICIDADE>, <MARCADORES>.

### 2.5 Validações
- Campos obrigatórios; URLs; duplicidade; existência de destino; consistência do resultado.

### 2.6 Persistência
- Estado da conversa: <PicklePersistence/JSON>.
- Histórico: <JSONL/arquivo>.

### 2.7 Rollback
- `<comando>` de restauração a partir de `backup/`.

### 2.8 Multi-usuário e sincronização
- `TELEGRAM_ALLOWED_USER_IDS`; `asyncio.Lock`; `git pull --ff-only` antes de editar; recheck de hash.

### 2.9 Versões e ambiente
- Python 3.12; `python-telegram-bot>=20`; `pydantic>=2`; `pytest`.

### 2.10 Idioma e fuso
- pt-BR; `America/Belem`.

---

## 3. Pendências / conflitos

1. <PENDÊNCIA> — <status>

---

## 4. Estrutura de pastas proposta

```
<NOME_PROJETO>/
├── AGENTS.md
├── CHANGELOG.md
├── README.md
├── .gitignore
├── bot/
├── backup/
├── docs/
└── <PASTA_DE_DADOS>/
```

---

## 5. Variáveis de ambiente (`.env`)

| Variável | Descrição |
|---|---|
| `TELEGRAM_BOT_TOKEN` | token do bot |
| `TELEGRAM_ALLOWED_USER_IDS` | IDs autorizados |
| `<OUTRAS>` | <descrição> |

---

## 6. Próximos passos

1. Resolver pendências da seção 3.
2. Estrutura de pastas + git + `.gitignore`.
3. `AGENTS.md` e `CHANGELOG.md`.
4. Esqueleto `bot/` e testes.
5. Documentação e deploy.
