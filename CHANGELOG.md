# Changelog

> Convenção: skill `changelog-convention`.
> Ordem **cronológica decrescente**; **não** misturar séries de numeração sem a nota + divisor.

## [Unreleased]

### v0.1.0 (21/10/2026) — Skill criada e validada (iteration-1)

- **Adicionado:** `SKILL.md` (metodologia fases 0–7, princípios, checklist de kickoff, anti-padrões).
- **Adicionado:** `references/` — `fase-requisitos.md`, `arquitetura-bot.md`, `politicas.md`,
  `deploy-systemd.md`.
- **Adicionado:** `assets/templates/` — AGENTS, CHANGELOG, requisitos, prompt-inicial, gitignore,
  requirements, pytest, env.example (+ `README.md` de índice).
- **Adicionado:** `scripts/bootstrap.py` — scaffold idempotente (pastas + templates), com `--dry-run`.
- **Adicionado:** `evals/evals.json` — 3 casos de teste.
- **Validado:** `bootstrap.py` compila e gera a estrutura substituindo placeholders; `evals.json` válido.
- **Validado:** benchmark `iteration-1` (3 evals × with_skill/without_skill) — with-skill **100%** vs
  baseline **67%** (delta **+0.33**); feedback do viewer **vazio** (aprovado).
- **Observação:** o `eval-3` (pedidos JSON) não discriminou (baseline 100%) porque o enunciado já
  continha os requisitos — candidato a ajuste de prompt/assertions em iteração futura.
- **Pendente:** otimização da `description` (via `run_loop.py`).
- **Arquivos:** `SKILL.md`, `references/`, `assets/templates/`, `scripts/bootstrap.py`,
  `evals/evals.json`; workspace de avaliação em `~/projetos/criacao-bot-telegram-workspace/`.

---

## Legenda

- **Adicionado** — novas funcionalidades
- **Alterado** — mudanças em funcionalidades existentes
- **Corrigido** — correções de bugs
- **Removido** — funcionalidades removidas
- **Segurança** — correções de vulnerabilidades
- **Obsoleto** — funcionalidades marcadas para remoção futura
