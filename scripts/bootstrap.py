#!/usr/bin/env python3
"""Scaffold de um novo projeto de bot Telegram a partir dos templates da skill.

Cria a estrutura de pastas e copia os templates, substituindo os placeholders conhecidos.
É idempotente: rodar duas vezes não sobrescreve arquivos já existentes (use --force para isso).
Use --dry-run para apenas visualizar o que seria feito.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"

# mapeamento: template -> destino relativo ao projeto
COPIES = {
    "prompt-inicial.template.md": "docs/prompt-inicial.md",
    "requisitos.template.md": "docs/requisitos.md",
    "AGENTS.template.md": "AGENTS.md",
    "CHANGELOG.template.md": "CHANGELOG.md",
    "gitignore.template": ".gitignore",
    "requirements.template.txt": "bot/requirements.txt",
    "pytest.template.ini": "pytest.ini",
    "env.example.template": "bot/.env.example",
}

DIRS = [
    "bot/handlers",
    "bot/models",
    "bot/schemas",
    "bot/services",
    "bot/tests",
    "backup",
    "docs",
]

GITKEEP = ["backup/.gitkeep", "bot/.gitkeep"]


def build_substitutions(name: str, remote: str, data_dir: str, date: str) -> dict[str, str]:
    return {
        "<NOME_PROJETO>": name,
        "<REMOTE_URL>": remote,
        "<PASTA_DE_DADOS>": data_dir,
        "<DATA>": date,
    }


def apply_substitutions(text: str, subs: dict[str, str]) -> str:
    for key, value in subs.items():
        text = text.replace(key, value)
    return text


def run(args: argparse.Namespace) -> int:
    root = Path(args.project_dir).expanduser().resolve()
    subs = build_substitutions(args.name, args.remote, args.data_dir, args.date)

    actions: list[str] = []

    if not TEMPLATES_DIR.is_dir():
        print(f"ERRO: templates não encontrados em {TEMPLATES_DIR}", file=sys.stderr)
        return 2

    for rel in DIRS:
        actions.append(f"mkdir -p {root / rel}")
    if args.data_dir:
        actions.append(f"mkdir -p {root / args.data_dir}")

    for rel in GITKEEP:
        actions.append(f"touch {root / rel}")

    for template, dest in COPIES.items():
        actions.append(f"gerar {root / dest}  (de {template})")

    if args.dry_run:
        print("== bootstrap.py --dry-run ==")
        print(f"projeto: {root}")
        for line in actions:
            print(f"  - {line}")
        print("Nada foi escrito (--dry-run).")
        return 0

    root.mkdir(parents=True, exist_ok=True)

    for rel in DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)
    if args.data_dir:
        (root / args.data_dir).mkdir(parents=True, exist_ok=True)

    for rel in GITKEEP:
        target = root / rel
        if not target.exists():
            target.touch()

    created, skipped = 0, 0
    for template, dest in COPIES.items():
        src = TEMPLATES_DIR / template
        dst = root / dest
        if dst.exists() and not args.force:
            print(f"  = já existe, mantido: {dest}")
            skipped += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = apply_substitutions(src.read_text(encoding="utf-8"), subs)
        dst.write_text(content, encoding="utf-8")
        print(f"  + criado: {dest}")
        created += 1

    print()
    print(f"Concluído: {created} arquivo(s) criado(s), {skipped} mantido(s).")
    print()
    print("Próximos passos:")
    print(f"  cd {root}")
    print("  git init -b main && git remote add origin <REMOTE_URL>")
    print("  # revisar e preencher os <PLACEHOLDERS> restantes nos arquivos gerados")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold de projeto de bot Telegram.")
    parser.add_argument("--project-dir", required=True, help="pasta onde o projeto será criado")
    parser.add_argument("--name", default="<NOME_PROJETO>", help="nome do projeto/bot")
    parser.add_argument("--data-dir", default="", help="pasta/clone da fonte de dados")
    parser.add_argument("--remote", default="<REMOTE_URL>", help="URL do repositório git do projeto")
    parser.add_argument("--date", default="<DATA>", help="data no formato DD/MM/AAAA")
    parser.add_argument("--force", action="store_true", help="sobrescrever arquivos existentes")
    parser.add_argument("--dry-run", action="store_true", help="apenas mostrar o que seria feito")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
