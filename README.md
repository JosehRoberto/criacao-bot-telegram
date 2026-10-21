# criacao-bot-telegram

Skill no padrão **[Agent Skills](https://agentskills.io)** com a metodologia para **criar e iniciar
um novo projeto de bot no Telegram**: objetivo, requisitos e decisões, estrutura de pastas,
`AGENTS.md`, `CHANGELOG.md`, `.gitignore`, esqueleto de código (`bot/`), testes e deploy via systemd.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `SKILL.md` | Metodologia (fases 0–7), princípios, checklist de kickoff e anti-padrões. |
| `references/` | Detalhes por tema: requisitos, arquitetura, políticas, deploy. |
| `assets/templates/` | Modelos prontos para copiar em projetos novos. |
| `scripts/bootstrap.py` | Scaffold idempotente (pastas + templates), com `--dry-run`. |
| `evals/evals.json` | Casos de teste da própria skill. |

## Uso rápido

O agente deve carregar a skill automaticamente ao detectar pedidos de criação de bot Telegram.
O caminho determinístico é rodar o scaffold:

```bash
python3 scripts/bootstrap.py --project-dir <destino> --name <nome> \
    --data-dir <pasta-de-dados> --remote <url-do-repo> --date DD/MM/AAAA
```

Use `--dry-run` para revisar antes. Os arquivos gerados ainda têm placeholders (`<OBJETIVO>`,
`<CAMPOS>`, ...) para preencher conforme o objetivo do bot.

## Instalação

Segue o padrão **Agent Skills** (`SKILL.md` com frontmatter `name`/`description`). Local global
recomendado neste computador: `/home/roberto/.config/opencode/skills/criacao-bot-telegram/`.

## Fontes

- Arquitetura/padrões de referência: `/home/roberto/projetos/agendatipara-bot` (somente leitura).
- Convenção de changelog: skill `changelog-convention`.
