# Templates da skill `criacao-bot-telegram`

Modelos prontos para copiar em um projeto novo. Os placeholders são substituídos pelo
`scripts/bootstrap.py` quando aplicável; os demais devem ser preenchidos pela IA/usuário.

| Arquivo | Destino no projeto | Substituições do bootstrap |
|---|---|---|
| `prompt-inicial.template.md` | `docs/prompt-inicial.md` | `<NOME_PROJETO>` |
| `requisitos.template.md` | `docs/requisitos.md` | `<NOME_PROJETO>`, `<REMOTE_URL>`, `<PASTA_DE_DADOS>` |
| `AGENTS.template.md` | `AGENTS.md` | `<NOME_PROJETO>`, `<REMOTE_URL>`, `<PASTA_DE_DADOS>` |
| `CHANGELOG.template.md` | `CHANGELOG.md` | `<DATA>` |
| `gitignore.template` | `.gitignore` | `<PASTA_DE_DADOS>` |
| `requirements.template.txt` | `bot/requirements.txt` | — |
| `pytest.template.ini` | `pytest.ini` | — |
| `env.example.template` | `bot/.env.example` | — |

## Placeholders

- `<NOME_PROJETO>` — nome do projeto/bot.
- `<REMOTE_URL>` — URL do repositório git do projeto.
- `<PASTA_DE_DADOS>` — pasta/clone do recurso que o bot manipula.
- `<DATA>` — data no formato `DD/MM/AAAA`.

Os demais placeholders em maiúsculas (`<OBJETIVO>`, `<CAMPO_1>`, `<VAR>`, ...) devem ser preenchidos
manualmente conforme o objetivo do novo bot.
