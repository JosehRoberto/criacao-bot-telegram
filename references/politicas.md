# Políticas do projeto

Regras que protegem o bot em produção e padronizam o trabalho de agentes. Adapte os **nomes de
arquivo** ao projeto; mantenha o **espírito** das regras.

## 1. Backup (pré-condição de escrita)

Nenhuma escrita em arquivo de produção acontece sem backup confirmado.

```bash
mkdir -p backup
TS=$(date +%Y%m%d_%H%M%S)
cp <arquivo-de-producao> backup/<nome>_${TS}.bak
ls -lh backup/<nome>_${TS}.bak   # confirmar antes de editar
```

- Fuso horário: `America/Belem`. Vários arquivos da mesma operação usam o **mesmo timestamp**.
- Rollback: `cp backup/<nome>_<TS>.bak <arquivo-de-producao>`.
- Manter os backups das últimas **5 sessões**; **nunca** commitar `backup/` nem `*.bak`.
- Quando o bot é quem escreve, o **serviço de backup** executa isso automaticamente antes de cada
  alteração — e o backup é uma região protegida (com teste).

## 2. Testes herméticos (obrigatório)

- Sem `.env` real, sem rede, sem escrever em arquivos de produção.
- Isolar caminhos com `tmp_path` + `monkeypatch` (README/alvo, `backup/`, histórico, JSON de estado).
- Mockar **todo** serviço externo: `requests.*` (APIs), `subprocess.run(["git", ...])`, API do
  Telegram. Nunca usar token/credencial real.
- Proibido em testes: `os.getenv`/`os.environ` direto; `requests.*` sem `patch`; `subprocess.run`
  sem mock; escrever em caminhos de produção sem `monkeypatch`.

Exemplo de isolamento:
```python
@pytest.fixture
def svc(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "README_PATH", tmp_path / "README.md")
    monkeypatch.setattr(mod, "BACKUP_DIR", tmp_path / "backup")
    return Servico()
```

## 3. `ConversationHandler` (python-telegram-bot v20+)

- **Nunca** registrar `CallbackQueryHandler` global para callbacks tratados **dentro** do
  `ConversationHandler` — o global intercepta e quebra o fluxo.
- A ordem dos estados vive no `state_manager`; mudá-la exige atualizar o dicionário de perguntas e o
  preview.
- `post_init` é atribuído **uma única vez** em `create_application()`; não reatribuir em `main.py`.
- Em testes de handlers, `application.updater = None` para não inicializar o bot real.

## 4. Git e publicação

- **Commit/push/MR só sob solicitação explícita.** O agente sugere a mensagem e aguarda autorização.
- Desenvolver direto em `main` (projeto simples). Branch curta só para experimentos.
- Mensagem de commit:
  ```
  [tipo]: [o que mudou em uma linha]

  [Por que foi necessário — contexto que o diff não mostra]
  [Qual problema resolve]
  ```
  Tipos: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.
- Um commit por tema; `docs:` pode ser separado do código.
- Nunca commitar: `.env`, `*.env` (exceto `.example`), dados clonados, `backup/`, `*.bak`, `.venv/`,
  `__pycache__/`.
- Tags anotadas `vX.Y[.Z]` com mensagem `deploy validado: <resumo>` (§15 do `AGENTS.md`).
- Rollback: preferir `git revert`; `git checkout <tag> -- <arquivo>` para arquivo isolado; nunca
  `reset --hard` em `main` publicada.

## 5. Operações no recurso de destino (git/API)

Commit/branch/push/MR no repositório alvo ou escrita em API externa são feitos pelo **serviço do
bot** e exigem **confirmação explícita do usuário no Telegram**. O agente nunca executa isso sozinho.

## 6. Níveis de risco

- **Baixo** (texto de mensagem, log): aplicar após validação.
- **Médio** (handlers, fluxo): validar localmente antes.
- **Alto** (`ConversationHandler`, parser/editor do alvo, modelo de dados, dependências): testar o
  fluxo completo `/start → … → Aprovar` antes de concluir.

## 7. Protocolos por tipo de tarefa

- **Diagnóstico de bug:** explicar o comportamento atual, o esperado e a divergência — e **só** propor
  correção após o usuário confirmar o diagnóstico.
- **Refatoração:** receber **um** critério (`legibilidade`, `performance` ou `estabilidade`), não
  alterar comportamento e comentar cada mudança conforme o critério.

## 8. Execução segura

- Trabalhar em etapas pequenas; confirmar o conteúdo real do arquivo antes de concluir.
- Nunca deixar código parcial, imports órfãos ou blocos abertos.
- Após interrupção/truncamento: inspecionar o estado real, corrigir de forma idempotente, não repetir
  cegamente a última ação nem duplicar blocos.
- Validar ao final: `python3 -m py_compile`, imports e `pytest`.
